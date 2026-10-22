"""Steps a position and a velocity of 32-bit float Vector3 values through 5 million sum, scale, cross and normalize steps."""
import math
import struct
import sys
import time

_float = struct.Struct("f")


def f32(value):
    return _float.unpack(_float.pack(value))[0]


class Vector3:
    def __init__(self, x, y, z):
        self.x = f32(x)
        self.y = f32(y)
        self.z = f32(z)


def sum_of(left, right):
    return Vector3(left.x + right.x, left.y + right.y, left.z + right.z)


def scaled(vector, factor):
    factor = f32(factor)
    return Vector3(vector.x * factor, vector.y * factor, vector.z * factor)


def squared_length(vector):
    return f32(f32(f32(vector.x * vector.x) + f32(vector.y * vector.y)) + f32(vector.z * vector.z))


def dot(left, right):
    return f32(f32(f32(left.x * right.x) + f32(left.y * right.y)) + f32(left.z * right.z))


def cross(left, right):
    return Vector3(f32(left.y * right.z) - f32(left.z * right.y),
                   f32(left.z * right.x) - f32(left.x * right.z),
                   f32(left.x * right.y) - f32(left.y * right.x))


def length(vector):
    return f32(math.sqrt(squared_length(vector)))


def normalized(vector):
    squared = squared_length(vector)
    if squared == 0.0:
        return Vector3(0.0, 0.0, 0.0)
    size = f32(math.sqrt(squared))
    return Vector3(vector.x / size, vector.y / size, vector.z / size)


def main():
    start = time.perf_counter_ns()
    position = Vector3(0.0, 0.0, 0.0)
    velocity = Vector3(1.0, 0.5, 0.25)
    axis = Vector3(0.0, 1.0, 0.0)
    total = 0.0
    for step in range(5000000):
        moved = scaled(velocity, 0.001)
        position = sum_of(position, moved)
        turned = cross(velocity, axis)
        nudged = sum_of(velocity, scaled(turned, 0.0001))
        velocity = normalized(nudged)
        total = f32(total + dot(position, velocity))
    checksum = int(total)
    ended = int(f32(length(position) * f32(1000.0)))
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"checksum {checksum} ended at {ended}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
