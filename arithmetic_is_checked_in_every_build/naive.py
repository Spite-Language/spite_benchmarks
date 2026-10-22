"""Checksums a list of 100000 numbers (value * 3 + round) over 400 rounds."""
import sys
import time


def checksum(values, round_number):
    total = 0
    for value in values:
        total = total + value * 3 + round_number
    return total


def rounds(values):
    total = 0
    for round_number in range(400):
        total = total + checksum(values, round_number)
    return total


def main():
    start = time.perf_counter_ns()
    values = []
    for index in range(100000):
        values.append(index % 1000)
    total = rounds(values)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
