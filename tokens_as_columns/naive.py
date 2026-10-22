"""Builds a text of pieces (--pieces=N), tokenises it into one Token object each, then counts kinds, totals the numbers and sums checksums."""
import sys
import time

IDENTIFIER = 0
NUMBER = 1
SYMBOL = 2

WORDS = ["alpha", "beta", "gamma", "delta", "value", "count", "index", "total"]
SYMBOLS = ["+", "=", "(", ")", ";", "*"]


class Token:
    def __init__(self, kind, start, length, line, value):
        self.kind = kind
        self.start = start
        self.length = length
        self.line = line
        self.value = value


def written(pieces):
    source = []
    seed = 7
    for index in range(pieces):
        seed = seed * 48271 % 2147483647
        choice = seed % 3
        picked = seed // 3 % 8
        if choice == 0:
            piece = WORDS[picked]
        elif choice == 1:
            piece = str(seed // 24 % 100000)
        else:
            piece = SYMBOLS[picked % 6]
        source.append(piece)
        source.append(" ")
        if index % 12 == 11:
            source.append("\n")
    return "".join(source).encode("ascii")


def tokenized(source):
    tokens = []
    length = len(source)
    line = 1
    position = 0
    while position < length:
        code = source[position]
        first = position
        if code == 10:
            line = line + 1
            position = position + 1
        elif code == 32:
            position = position + 1
        elif 97 <= code <= 122:
            hash_value = 0
            while position < length and 97 <= source[position] <= 122:
                hash_value = (hash_value * 31 + source[position]) % 1000000007
                position = position + 1
            tokens.append(Token(IDENTIFIER, first, position - first, line, hash_value))
        elif 48 <= code <= 57:
            number = 0
            while position < length and 48 <= source[position] <= 57:
                number = number * 10 + source[position] - 48
                position = position + 1
            tokens.append(Token(NUMBER, first, position - first, line, number))
        else:
            position = position + 1
            tokens.append(Token(SYMBOL, first, 1, line, code))
    return tokens


def count_kind(tokens, kind):
    count = 0
    for index in range(len(tokens)):
        if tokens[index].kind == kind:
            count = count + 1
    return count


def total_of_numbers(tokens):
    total = 0
    for index in range(len(tokens)):
        token = tokens[index]
        if token.kind == NUMBER:
            total = total + token.value
    return total


def checksum(token):
    total = token.start
    total = total + token.length * 7 + token.line * 13
    total = total + token.value % 1000
    return total


def setting_of(arguments, flag, otherwise):
    for argument in arguments:
        if argument.startswith(flag):
            return int(argument[len(flag):])
    return otherwise


def main():
    pieces = setting_of(sys.argv[1:], "--pieces=", 1500000)
    start = time.perf_counter_ns()
    source = written(pieces)
    wrote = time.perf_counter_ns()
    tokens = tokenized(source)
    tokenised = time.perf_counter_ns()
    identifiers = count_kind(tokens, IDENTIFIER)
    numbers = count_kind(tokens, NUMBER)
    symbol_count = count_kind(tokens, SYMBOL)
    number_total = total_of_numbers(tokens)
    checksums = 0
    for index in range(len(tokens)):
        checksums = checksums + checksum(tokens[index])
    finished = time.perf_counter_ns()
    print(f"identifiers {identifiers} numbers {numbers} symbols {symbol_count} number total {number_total} checksums {checksums}")
    print(f"microseconds {(finished - start) // 1000}", file=sys.stderr)
    print(f"phases write {(wrote - start) // 1000} tokenise {(tokenised - wrote) // 1000} passes {(finished - tokenised) // 1000}", file=sys.stderr)


if __name__ == "__main__":
    main()
