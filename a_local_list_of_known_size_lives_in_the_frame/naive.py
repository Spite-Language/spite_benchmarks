"""Builds two small lists per call from list literals and finds the largest weighted remainder, ten million times."""
import sys
import time


def largest_remainder(round_number):
    remainders = [round_number % 10, round_number % 7, round_number % 13, round_number % 3]
    weights = [4, 3, 2, 1]
    biggest = 0
    for index in range(len(remainders)):
        weighted = remainders[index] * weights[index]
        if weighted > biggest:
            biggest = weighted
    return biggest


def all_rounds(rounds):
    total = 0
    for round_number in range(rounds):
        biggest = largest_remainder(round_number)
        total = total + biggest
    return total


def main():
    start = time.perf_counter_ns()
    total = all_rounds(10000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
