"""Simulates 20 million steps of a position, velocity and gravity, each step making new offset objects (single precision floats, rounded after every operation like C floats)."""
import struct
import sys
import time

SINGLE = struct.Struct("f")


def single(value):
    return SINGLE.unpack(SINGLE.pack(value))[0]


class Offset:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def sum(self, other):
        return Offset(single(self.x + other.x), single(self.y + other.y), single(self.z + other.z))

    def scaled(self, factor):
        return Offset(single(self.x * factor), single(self.y * factor), single(self.z * factor))


def simulate(steps):
    position = Offset(0.0, 0.0, 0.0)
    velocity = Offset(1.0, 0.5, 0.25)
    gravity = Offset(0.0, -0.5, 0.0)
    pull = single(0.000001)
    move = single(0.001)
    for step in range(steps):
        pulled = gravity.scaled(pull)
        velocity = velocity.sum(pulled)
        moved = velocity.scaled(move)
        position = position.sum(moved)
    return position


def main():
    start = time.perf_counter_ns()
    ended = simulate(20000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    across = int(single(ended.x * 1000.0))
    up = int(single(ended.y * 1000.0))
    ahead = int(single(ended.z * 1000.0))
    print(f"ended at {across} {up} {ahead}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
