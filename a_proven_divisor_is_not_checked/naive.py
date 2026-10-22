"""Share a million amounts into parts over 20 rounds, adding each quotient and remainder."""
import sys
import time


def shares(amounts, parts):
    total = 0
    for amount in amounts:
        total = total + amount // parts + amount % parts
    return total


def rounds(amounts):
    total = 0
    for round in range(20):
        parts = round % 7 + 1
        shared = shares(amounts, parts)
        total = total + shared
    return total


def main():
    start = time.perf_counter_ns()
    amounts = []
    for index in range(1000000):
        amounts.append(index % 9973)
    total = rounds(amounts)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
