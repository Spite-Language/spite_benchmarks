"""A meter reads from a list of readings and adds the offset of its settings limits, ten million times."""
import sys
import time


class Limits:
    def __init__(self, offset):
        self.offset = offset


class Settings:
    def __init__(self, limits):
        self.limits = limits


class Meter:
    def __init__(self, settings):
        self.readings = []
        self.settings = settings

    def reading_at(self, values, at):
        if at < 0 or at >= len(values):
            raise IndexError(at)
        return values[at]

    def offset_of(self, limits):
        return limits.offset

    def measure(self, at):
        return self.reading_at(self.readings, at % 16) + self.offset_of(self.settings.limits)

    def measure_all(self, count):
        total = 0
        for index in range(count):
            total = total + self.measure(index)
        return total


def main():
    meter = Meter(Settings(Limits(3)))
    for index in range(16):
        meter.readings.append(index)
    start = time.perf_counter_ns()
    total = meter.measure_all(10000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
