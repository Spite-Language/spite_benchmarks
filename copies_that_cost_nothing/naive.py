"""Copies a point twenty million times, moves each copy and adds up its distance from the origin."""
import sys
import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)


def move_by(point, across, down):
    point.x = point.x + across
    point.y = point.y + down


def distance_from_origin(point):
    return abs(point.x) + abs(point.y)


def all_trials(origin, trials):
    total = 0
    for trial in range(trials):
        moved = origin.copy()
        move_by(moved, trial % 7 - 3, trial % 5 - 2)
        total = total + distance_from_origin(moved)
    return total


def main():
    start = time.perf_counter_ns()
    origin = Point(3, -4)
    total = all_trials(origin, 20000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total} origin {origin.x} {origin.y}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
