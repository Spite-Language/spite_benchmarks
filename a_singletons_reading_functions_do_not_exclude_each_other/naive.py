"""Eight threads per tick read every row of a shared list of transforms through a lock, for 20 ticks (threading, as a Python programmer shares an object between threads)."""
import sys
import threading
import time

ROW_TOTAL = 15000
SYSTEM_COUNT = 8


class Transform:
    def __init__(self, across):
        self.across = across


class Transforms:
    def __init__(self):
        self.stored = []
        self.lock = threading.Lock()

    def insert(self, transform):
        with self.lock:
            self.stored.append(transform)

    def at(self, row):
        with self.lock:
            if row < 0 or row >= len(self.stored):
                raise IndexError(row)
            return self.stored[row]


class System:
    def __init__(self, transforms, rows):
        self.transforms = transforms
        self.rows = rows
        self.result = 0

    def run(self):
        total = 0
        for row in range(self.rows):
            transform = self.transforms.at(row)
            total = total + transform.across
        self.result = total


def one_tick(transforms):
    systems = []
    threads = []
    for index in range(SYSTEM_COUNT):
        system = System(transforms, ROW_TOTAL)
        thread = threading.Thread(target=system.run)
        systems.append(system)
        threads.append(thread)
        thread.start()
    total = 0
    for index in range(SYSTEM_COUNT):
        threads[index].join()
        total = total + systems[index].result
    return total


def ticks(transforms, count):
    total = 0
    for tick in range(count):
        total = total + one_tick(transforms)
        written = transforms.at(tick)
        transforms.insert(written)
    return total


def main():
    transforms = Transforms()
    start = time.perf_counter_ns()
    for row in range(ROW_TOTAL):
        transforms.insert(Transform(row % 1000))
    total = ticks(transforms, 20)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
