"""Restocks a rack of sixteen crate slots ten million times, reading the weight in a slot before storing a crate there."""
import sys
import time


class Crate:
    def __init__(self, weight):
        self.weight = weight


class Rack:
    def __init__(self, light, heavy):
        self.light = light
        self.heavy = heavy
        self.crates = [light] * 16

    def place(self, at, crate):
        before = self.crates[at].weight
        self.crates[at] = crate
        return 0 if before == crate.weight else 1

    def restock(self, count):
        changed = 0
        for index in range(count):
            at = index % 16
            if index % 64 == 0:
                changed = changed + self.place(at, self.heavy)
            else:
                changed = changed + self.place(at, self.light)
        return changed


def main():
    rack = Rack(Crate(2), Crate(9))
    start = time.perf_counter_ns()
    changed = rack.restock(10000000)
    total = 0
    for index in range(len(rack.crates)):
        total = total + rack.crates[index].weight
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"changed {changed} total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
