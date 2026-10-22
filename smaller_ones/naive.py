"""Calls a bound method on each of a million numbers, 50 times, through a function value passed to each()."""
import sys
import time


class Tally:
    def __init__(self):
        self.total = 0
        self.large = 0

    def count_value(self, value):
        self.total = self.total + value
        if value > 900:
            self.large = self.large + 1


def each(values, function):
    for value in values:
        function(value)


def main():
    start = time.perf_counter_ns()
    values = []
    for index in range(1000000):
        values.append(index % 1000)
    tally = Tally()
    for round_number in range(50):
        each(values, tally.count_value)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {tally.total} large {tally.large}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
