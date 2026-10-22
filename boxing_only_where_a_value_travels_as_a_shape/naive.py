"""A list of printable values (integers, booleans, texts) turned to text and measured, 20 rounds."""
import sys
import time


class Integer:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return str(self.value)


class Boolean:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return "true" if self.value else "false"


class Text:
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return self.value


def add_value(values, index):
    kind = index % 3
    if kind == 0:
        values.append(Integer(index))
    elif kind == 1:
        values.append(Boolean(index % 2 == 0))
    else:
        values.append(Text(f"item {index}"))


def make_values(count):
    values = []
    for index in range(count):
        add_value(values, index)
    return values


def measure(values):
    total = 0
    for value in values:
        total = total + len(value.to_string())
    return total


def measure_rounds(values):
    total = 0
    for round in range(20):
        length = measure(values)
        total = total + length
    return total


def main():
    start = time.perf_counter_ns()
    values = make_values(90000)
    total = measure_rounds(values)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
