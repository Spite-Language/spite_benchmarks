"""Fills a dictionary keyed by numbers, then looks numbers up in it for 40 rounds and adds up what it finds."""
import sys
import time


def key_of(index):
    return index * 7919 % 1000003


def make_table(count):
    by_number = {}
    for index in range(count):
        key = key_of(index)
        by_number[key] = index * 2
    return by_number


def look_up(by_number, count):
    total = 0
    for round_number in range(40):
        for index in range(count):
            key = key_of(index + round_number)
            found = by_number.get(key)
            if found is not None:
                total = total + found
    return total


def main():
    start = time.perf_counter_ns()
    by_number = make_table(100000)
    total = look_up(by_number, 100000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total} entries {len(by_number)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
