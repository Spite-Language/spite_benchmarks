"""Measures integers, floats, crates and balls through one function that takes any measurable value."""
import sys
import time


class Crate:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

    def to_double(self):
        return float(self.width * self.height * self.depth)


class Ball:
    def __init__(self, radius):
        self.radius = radius

    def to_double(self):
        return float(self.radius + self.radius)


def measured_to_double(value):
    if isinstance(value, (int, float)):
        return float(value)
    return value.to_double()


def doubled(value):
    measure = measured_to_double(value)
    return measure + measure


def measure_all(steps):
    total = 0.0
    crate = Crate(1.0, 2.0, 3.0)
    ball = Ball(1.0)
    for step in range(steps):
        total = total + doubled(step % 10)
        total = total + doubled(float(step % 4))
        crate.width = float(step % 7)
        total = total + doubled(crate)
        ball.radius = float(step % 5)
        total = total + doubled(ball)
    return total


def main():
    start = time.perf_counter_ns()
    total = measure_all(20000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {int(total)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
