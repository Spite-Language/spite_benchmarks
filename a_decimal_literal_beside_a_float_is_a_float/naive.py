"""Sums a list of 32-bit floats through (value + shift) * 1.5 + 0.25 over many rounds, narrowing each result to float."""
import struct
import sys
import time

_float = struct.Struct("f")


def f32(value):
    return _float.unpack(_float.pack(value))[0]


def scaled_sum(values, shift):
    total = 0.0
    for item in values:
        # the literals are doubles: the float is widened, the answer narrowed to store it
        total = f32(total + f32(item + shift) * 1.5 + 0.25)
    return total


def rounds(values):
    total = 0.0
    for round_number in range(4000):
        shift = float(round_number % 8)
        total = total + scaled_sum(values, shift)
    return total


def main():
    start = time.perf_counter_ns()
    values = []
    for index in range(50000):
        quarters = float(index % 64)
        values.append(f32(quarters * 0.25))
    total = rounds(values)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {int(total)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
