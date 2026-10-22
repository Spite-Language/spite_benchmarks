"""Sums on a worker threading.Thread while the main thread keeps the points past a threshold, twenty times."""
import sys
import threading
import time


class Summer:
    def __init__(self, limit):
        self.limit = limit
        self.result = 0

    def total(self):
        total = 0
        for index in range(self.limit):
            total = total + index % 7
        return total

    def thread_main(self):
        self.result = self.total()


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
    summer = Summer(20000000)
    thread = threading.Thread(target=summer.thread_main)
    thread.start()
    points = make_points(200000)
    near_count = count_near(points)
    thread.join()
    total = summer.result
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"sum {total} near {near_count}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
