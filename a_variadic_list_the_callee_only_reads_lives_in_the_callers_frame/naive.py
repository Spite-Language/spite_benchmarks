"""Find the largest of four values 2000000 times, the values arriving in a list."""
import sys
import time


def largest(*values):
    biggest = 0
    for value in values:
        if value > biggest:
            biggest = value
    return biggest


def all_rounds(rounds):
    total = 0
    for round in range(rounds):
        biggest = largest(round % 10, round % 7, round % 13, round % 3)
        total = total + biggest
    return total


def main():
    start = time.perf_counter_ns()
    total = all_rounds(2000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
