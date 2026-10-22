"""Keeps the points of a list whose across plus down is past a threshold, twenty times, and counts them."""
import sys
import time


class Point:
    def __init__(self, across, down):
        self.across = across
        self.down = down


def make_points(count):
    points = []
    for index in range(count):
        points.append(Point(index % 1000, index % 700))
    return points


def count_near(points):
    near_count = 0
    for round in range(20):
        kept = []
        for point in points:
            if point.across + point.down > round * 80:
                kept.append(point)
        near_count = near_count + len(kept)
    return near_count


def main():
    start = time.perf_counter_ns()
    points = make_points(200000)
    near_count = count_near(points)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"near {near_count}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
