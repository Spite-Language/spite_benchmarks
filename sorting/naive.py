"""Fills a list with two million pseudo-random numbers, sorts it with list.sort() and checks the order."""
import sys
import time


def main():
    start = time.perf_counter_ns()
    count = 2000000
    numbers = []
    seed = 42
    for _ in range(count):
        seed = seed * 48271 % 2147483647
        numbers.append(seed % 1000000)
    numbers.sort()
    checksum = 0
    ordered = True
    for index in range(count):
        checksum = checksum + numbers[index] * (index % 7)
        if index > 0 and numbers[index - 1] > numbers[index]:
            ordered = False
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"ordered {'true' if ordered else 'false'} checksum {checksum}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
