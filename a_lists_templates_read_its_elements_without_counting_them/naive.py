"""Advance 200000 bodies for 100 rounds, summing their positions, and sum a list of labels."""
import sys
import time


class Body:
    def __init__(self, speed):
        self.position = 0
        self.speed = speed

    def advance(self):
        self.position = self.position + self.speed


class Label:
    def __init__(self, number):
        self.number = number


def each_advance(bodies):
    for body in bodies:
        body.advance()


def sum_position(bodies):
    total = 0
    for body in bodies:
        total = total + body.position
    return total


def sum_number(labels):
    total = 0
    for label in labels:
        total = total + label.number
    return total


def simulate(bodies):
    total = 0
    for round in range(100):
        each_advance(bodies)
        positions = sum_position(bodies)
        total = total + positions
    return total


def main():
    start = time.perf_counter_ns()
    bodies = []
    labels = []
    for index in range(200000):
        bodies.append(Body(index % 5 + 1))
        labels.append(Label(index % 10))
    total = simulate(bodies)
    numbers = sum_number(labels)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total} labels {numbers}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
