"""Slides a window over a list of numbers and counts rises, for 300 rounds, adding up the results."""
import sys
import time


def wrap32(value):
    value &= 0xFFFFFFFF
    return value - 0x100000000 if value >= 0x80000000 else value


def window_total(values, weight):
    total = 0
    at = 0
    while at + 2 < len(values):
        total = wrap32(total + values[at] * weight + values[at + 1] + values[at + 2])
        at = at + 1
    return total


def rise_count(values, threshold):
    count = len(values)
    rises = 0
    previous = 0
    index = 0
    while index < count:
        value = values[index]
        if value - previous > threshold:
            rises = rises + 1
        previous = value
        index = index + 1
    return rises


def rounds(values):
    total = 0
    for round_number in range(300):
        weight = round_number % 3 + 1
        windows = window_total(values, weight)
        threshold = round_number % 50
        rises = rise_count(values, threshold)
        total = total + windows + rises
    return total


def main():
    values = []
    for index in range(100000):
        values.append(index * 37 % 101)
    start = time.perf_counter_ns()
    total = rounds(values)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
