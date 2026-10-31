"""Advance 100000 orbits one after the other, ten times, with 32-bit float arithmetic as the C has."""
import struct
import sys
import time

_FLOAT = struct.Struct("f")


def single(value):
    # round to a 32-bit float, as C's float does after every operation
    return _FLOAT.unpack(_FLOAT.pack(value))[0]


class Orbit:
    def __init__(self, speed):
        self.angle = 0.0
        self.speed = speed
        self.turns = 0

    def advance(self):
        step_size = single(0.001)
        full_turn = single(6.2831855)
        for step in range(1000):
            self.angle = single(self.angle + single(self.speed * step_size))
            if self.angle > full_turn:
                self.angle = single(self.angle - full_turn)
                self.turns = self.turns + 1


def main():
    count = 100000
    orbits = [Orbit(float(index % 17 + 1)) for index in range(count)]
    start = time.perf_counter_ns()
    for tick in range(10):
        for orbit in orbits:
            orbit.advance()
    microseconds = (time.perf_counter_ns() - start) // 1000
    turns = 0
    for orbit in orbits:
        turns = turns + orbit.turns
    print(f"turns {turns}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
