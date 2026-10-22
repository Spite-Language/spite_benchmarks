"""Visits a hundred thousand columns for 100 rounds, hitting each and storing its weight in a list, then sums the hits."""
import sys
import time


class Column:
    def __init__(self, step):
        self.hits = 0
        self.step = step

    def hit(self):
        self.hits = self.hits + self.step


def weight(column):
    return column.hits * 10


def visit(columns, weights, index):
    column = columns[index]
    column.hit()
    weights[index] = weight(column)


def visit_all(columns, weights):
    for index in range(len(columns)):
        visit(columns, weights, index)


def sum_hits(columns):
    total = 0
    for index in range(len(columns)):
        total = total + columns[index].hits
    return total


def main():
    start = time.perf_counter_ns()
    columns = []
    weights = []
    for index in range(100000):
        columns.append(Column(index % 3 + 1))
        weights.append(0)
    for round_number in range(100):
        visit_all(columns, weights)
    hits = sum_hits(columns)
    last = weights[99999]
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"hits {hits} last weight {last}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
