"""Turns a hundred thousand points by half a radian 200 times, calling cos and sin on the constant each time, and sums the across values (single precision floats, rounded after every operation like C floats)."""
import math
import struct
import sys
import time

SINGLE = struct.Struct("f")


def single(value):
    return SINGLE.unpack(SINGLE.pack(value))[0]


class Point:
    def __init__(self, across, down):
        self.across = across
        self.down = down


def make_points(count):
    points = []
    for index in range(count):
        points.append(Point(float(index % 100), float(index % 37)))
    return points


def turn(point):
    turned_across = single(single(point.across * single(math.cos(0.5))) - single(point.down * single(math.sin(0.5))))
    turned_down = single(single(point.across * single(math.sin(0.5))) + single(point.down * single(math.cos(0.5))))
    point.across = turned_across
    point.down = turned_down


def sum_across(points):
    total = 0.0
    for index in range(len(points)):
        total = single(total + points[index].across)
    return total


def main():
    start = time.perf_counter_ns()
    points = make_points(100000)
    for round_number in range(200):
        for index in range(len(points)):
            turn(points[index])
    total = sum_across(points)
    whole = int(math.floor(abs(total) + 0.5))
    if total < 0:
        whole = -whole
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"across {whole}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
