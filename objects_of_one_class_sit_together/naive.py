"""Make points and notes in turn, each kept in its own list, and sum the points over 30 rounds."""
import sys
import time


class Point:
    def __init__(self, across, down):
        self.across = across
        self.down = down


class Note:
    def __init__(self, text):
        self.text = text


def make_both(points, notes, count):
    for index in range(count):
        points.append(Point(index % 1000, index % 30))
        notes.append(Note("made"))


def sum_points(points):
    total = 0
    for round in range(30):
        for point in points:
            if point.down >= round:
                total = total + point.across + point.down
    return total


def main():
    points = []
    notes = []
    start = time.perf_counter_ns()
    make_both(points, notes, 300000)
    total = sum_points(points)
    noted = len(notes)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total} notes {noted}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
