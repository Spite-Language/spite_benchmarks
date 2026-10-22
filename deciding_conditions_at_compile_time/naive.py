"""Adds a million values to a plain meter and a squaring meter, for 20 rounds; one Meter class tests its own flag on every add."""
import sys
import time


class Meter:
    def __init__(self, is_squared):
        self.is_squared = is_squared
        self.total = 0

    def add(self, value):
        if self.is_squared:
            square = value
            self.total = self.total + square * value
        else:
            self.total = self.total + value


def make_values(count):
    values = []
    for index in range(count):
        values.append(index % 1000)
    return values


def measure(values, plain, squared):
    for index in range(len(values)):
        value = values[index]
        plain.add(value)
        squared.add(value)


def main():
    start = time.perf_counter_ns()
    values = make_values(1000000)
    plain = Meter(False)
    squared = Meter(True)
    for round_number in range(20):
        measure(values, plain, squared)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"sum {plain.total} squares {squared.total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
