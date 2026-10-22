"""Moves a vector, multiplies rotation matrices and transforms points, rounding every operation to 32-bit floats as the C does."""
import math
import struct
import sys
import time

FLOAT = struct.Struct("<f")


def f32(value):
    return FLOAT.unpack(FLOAT.pack(value))[0]


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Quaternion:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w


class Matrix4:
    # columns[column][row]
    def __init__(self, columns):
        self.columns = columns

    @staticmethod
    def identity():
        return Matrix4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])

    def multiply(self, other):
        a = self.columns
        product = []
        for column in range(4):
            b = other.columns[column]
            entries = []
            for row in range(4):
                total = f32(a[0][row] * b[0])
                total = f32(total + f32(a[1][row] * b[1]))
                total = f32(total + f32(a[2][row] * b[2]))
                total = f32(total + f32(a[3][row] * b[3]))
                entries.append(total)
            product.append(entries)
        return Matrix4(product)

    def transform_point(self, point):
        m = self.columns
        x = f32(f32(f32(f32(m[0][0] * point.x) + f32(m[1][0] * point.y)) + f32(m[2][0] * point.z)) + m[3][0])
        y = f32(f32(f32(f32(m[0][1] * point.x) + f32(m[1][1] * point.y)) + f32(m[2][1] * point.z)) + m[3][1])
        z = f32(f32(f32(f32(m[0][2] * point.x) + f32(m[1][2] * point.y)) + f32(m[2][2] * point.z)) + m[3][2])
        return Vector3(x, y, z)


def vector3_sum(left, right):
    return Vector3(f32(left.x + right.x), f32(left.y + right.y), f32(left.z + right.z))


def vector3_scaled(vector, factor):
    return Vector3(f32(vector.x * factor), f32(vector.y * factor), f32(vector.z * factor))


def vector3_normalized(vector):
    squared = f32(f32(f32(vector.x * vector.x) + f32(vector.y * vector.y)) + f32(vector.z * vector.z))
    if squared == 0.0:
        return Vector3(0.0, 0.0, 0.0)
    inverse_length = f32(1.0 / f32(math.sqrt(squared)))
    return Vector3(f32(vector.x * inverse_length), f32(vector.y * inverse_length), f32(vector.z * inverse_length))


def quaternion_axis_angle(axis, angle):
    unit = vector3_normalized(axis)
    half_angle = f32(angle * 0.5)
    half_sine = f32(math.sin(half_angle))
    return Quaternion(f32(unit.x * half_sine), f32(unit.y * half_sine), f32(unit.z * half_sine),
                      f32(math.cos(half_angle)))


def quaternion_to_matrix(rotation):
    x_x = f32(rotation.x * rotation.x)
    y_y = f32(rotation.y * rotation.y)
    z_z = f32(rotation.z * rotation.z)
    x_y = f32(rotation.x * rotation.y)
    x_z = f32(rotation.x * rotation.z)
    y_z = f32(rotation.y * rotation.z)
    w_x = f32(rotation.w * rotation.x)
    w_y = f32(rotation.w * rotation.y)
    w_z = f32(rotation.w * rotation.z)
    result = Matrix4.identity()
    m = result.columns
    m[0][0] = f32(1.0 - 2.0 * f32(y_y + z_z))
    m[0][1] = f32(2.0 * f32(x_y + w_z))
    m[0][2] = f32(2.0 * f32(x_z - w_y))
    m[1][0] = f32(2.0 * f32(x_y - w_z))
    m[1][1] = f32(1.0 - 2.0 * f32(x_x + z_z))
    m[1][2] = f32(2.0 * f32(y_z + w_x))
    m[2][0] = f32(2.0 * f32(x_z + w_y))
    m[2][1] = f32(2.0 * f32(y_z - w_x))
    m[2][2] = f32(1.0 - 2.0 * f32(x_x + y_y))
    return result


def vector_pass():
    position = Vector3(0.0, 0.0, 0.0)
    velocity = Vector3(1.0, 0.5, 0.25)
    factor = f32(0.001)
    for _ in range(1000000):
        moved = vector3_scaled(velocity, factor)
        position = vector3_sum(position, moved)
    return position


def matrix_pass():
    axis = Vector3(0.0, 1.0, 0.0)
    step_matrix = quaternion_to_matrix(quaternion_axis_angle(axis, f32(0.001)))
    accumulated = Matrix4.identity()
    for _ in range(200000):
        accumulated = accumulated.multiply(step_matrix)
    m = accumulated.columns
    return f32(f32(m[0][0] + m[1][1]) + m[2][2])


def transform_pass():
    model = Matrix4.identity()
    model.columns[3][0] = 1.0
    model.columns[3][1] = 2.0
    model.columns[3][2] = 3.0
    point = Vector3(0.5, 0.5, 0.5)
    total = 0.0
    for _ in range(1000000):
        moved = model.transform_point(point)
        total = f32(total + moved.x)
    return total


def main():
    start = time.perf_counter_ns()
    moved = vector_pass()
    combined = matrix_pass()
    transformed = transform_pass()
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"ended at {int(f32(moved.x * 1000.0))} {int(f32(moved.y * 1000.0))} {int(f32(moved.z * 1000.0))} "
          f"diagonal {int(f32(combined * 1000000.0))} total {int(transformed)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
