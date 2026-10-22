"""Counts with two objects one after the other on the one thread (sequential: threading would not speed the work up in Python)."""
import sys
import time


class Evens:
    def __init__(self):
        self.total = 0

    def count(self):
        for index in range(40000000):
            self.total = self.total + index % 7 * 2


class Odds:
    def __init__(self):
        self.total = 0

    def count(self):
        for index in range(40000000):
            self.total = self.total + index % 5 * 2 + 1


def count_both(evens, odds):
    evens.count()
    odds.count()


def main():
    evens = Evens()
    odds = Odds()
    start = time.perf_counter_ns()
    count_both(evens, odds)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"{evens.total} {odds.total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
