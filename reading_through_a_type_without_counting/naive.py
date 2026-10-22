"""Moves a hundred thousand rows by their velocities for 200 ticks, each row read through a Moving shape that offers a position and a velocity."""
import sys
import time


class Position:
    def __init__(self, left, top):
        self.left = left
        self.top = top


class Velocity:
    def __init__(self, across, down):
        self.across = across
        self.down = down


class MovingRow:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


def advance(moving, steps):
    moving.position.left = moving.position.left + moving.velocity.across * steps
    moving.position.top = moving.position.top + moving.velocity.down * steps


def fill(positions, velocities, count):
    for index in range(count):
        positions.append(Position(0, 0))
        velocities.append(Velocity(index % 13 - 6, index % 7 - 3))


def ticks(positions, velocities):
    for tick in range(200):
        for index in range(len(positions)):
            moving = MovingRow(positions[index], velocities[index])
            advance(moving, tick % 3)


def sum_place(positions):
    total = 0
    for index in range(len(positions)):
        total = total + (positions[index].left + positions[index].top)
    return total


def main():
    start = time.perf_counter_ns()
    positions = []
    velocities = []
    fill(positions, velocities, 100000)
    ticks(positions, velocities)
    total = sum_place(positions)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
