"""Steps 100000 particles of 32-bit floats for 300 ticks with gravity and a bounce, then sums heights and spread."""
import struct
import sys
import time

_float = struct.Struct("f")


def f32(value):
    return _float.unpack(_float.pack(value))[0]


class Particle:
    def __init__(self):
        self.position_x = 0.0
        self.position_y = 0.0
        self.position_z = 0.0
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_z = 0.0


FALL = f32(9.8 * 0.016)
TICK = f32(0.016)
BOUNCE = f32(0.8)


def step(particle):
    particle.velocity_y = f32(particle.velocity_y - FALL)
    particle.position_x = f32(particle.position_x + f32(particle.velocity_x * TICK))
    particle.position_y = f32(particle.position_y + f32(particle.velocity_y * TICK))
    particle.position_z = f32(particle.position_z + f32(particle.velocity_z * TICK))
    if particle.position_y < 0.0:
        particle.position_y = -particle.position_y
        particle.velocity_y = f32(-particle.velocity_y * BOUNCE)


def main():
    start = time.perf_counter_ns()
    count = 100000
    particles = []
    for index in range(count):
        particle = Particle()
        particle.position_x = float(index % 100)
        particle.position_y = float(index % 37 + 1)
        particle.position_z = float(index % 53)
        particle.velocity_x = float(index % 7 - 3)
        particle.velocity_y = float(index % 11)
        particle.velocity_z = float(index % 5 - 2)
        particles.append(particle)
    for tick in range(300):
        for particle in particles:
            step(particle)
    height = 0.0
    spread = 0.0
    for particle in particles:
        height = f32(height + particle.position_y)
        spread = f32(f32(spread + particle.position_x) + particle.position_z)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"height {int(height)} spread {int(spread)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
