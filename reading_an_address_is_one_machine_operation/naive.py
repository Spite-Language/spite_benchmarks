"""Encode a list of 100000 bytes as base64 text 100 times, each digit written through a function of its own."""
import sys
import time

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def read_byte(address, offset):
    return address[offset]


def write_byte(address, offset, value):
    address[offset] = value


def write_digit(address, at, group, shift):
    value = (group >> shift) & 63
    write_byte(address, at, ALPHABET[value])
    return at + 1


def encode(data):
    count = len(data)
    room = (count + 2) // 3 * 4
    address = [""] * room
    written = 0
    for index in range(0, count, 3):
        group = read_byte(data, index) << 16
        present = count - index
        if present > 1:
            group = group | (read_byte(data, index + 1) << 8)
        if present > 2:
            group = group | read_byte(data, index + 2)
        written = write_digit(address, written, group, 18)
        written = write_digit(address, written, group, 12)
        if present > 1:
            written = write_digit(address, written, group, 6)
        else:
            write_byte(address, written, "=")
            written = written + 1
        if present > 2:
            written = write_digit(address, written, group, 0)
        else:
            write_byte(address, written, "=")
            written = written + 1
    return "".join(address)


def encode_rounds(data):
    total = 0
    for round in range(100):
        data[round] = round
        encoded = encode(data)
        total = total + len(encoded) + ord(encoded[round])
    return total


def main():
    start = time.perf_counter_ns()
    data = []
    for index in range(100000):
        data.append(index * 7 % 256)
    total = encode_rounds(data)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
