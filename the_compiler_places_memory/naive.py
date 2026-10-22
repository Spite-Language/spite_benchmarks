"""Sums the squares of 32 numbers a million times, each call holding its squares in a list of its own."""
import sys
import time


def sum_of_squares(count, offset):
    squares = [0] * count
    for index in range(count):
        value = index + offset
        squares[index] = value * value
    total = 0
    for index in range(count):
        total = total + squares[index]
    return total


def sum_rounds(rounds):
    total = 0
    for round_number in range(rounds):
        squares = sum_of_squares(32, round_number % 1000)
        total = total + squares
    return total


def main():
    start = time.perf_counter_ns()
    total = sum_rounds(1000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
