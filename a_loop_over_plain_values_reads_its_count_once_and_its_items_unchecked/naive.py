"""Scales a list of floats into another list and adds it up, two thousand times."""
import sys
import time


def scale_list(source, into, offset):
    for index in range(len(source)):
        into[index] = source[index] * 1.5 + offset


def add_up(values):
    total = 0.0
    for index in range(len(values)):
        total = total + values[index]
    return total


def rounds(source, into):
    total = 0
    for round in range(2000):
        offset = float(round % 4)
        offset = offset * 0.25
        scale_list(source, into, offset)
        total_sum = add_up(into)
        total += int(total_sum * 4.0)
    return total


def main():
    source = []
    into = []
    for index in range(100000):
        source.append(float(index % 7))
        into.append(0.0)
    start = time.perf_counter_ns()
    total = rounds(source, into)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total in quarters {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
