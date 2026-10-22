"""Makes 10000 particle objects per round for 200 rounds, sums their positions and speeds, and drops them."""
import sys
import time


class Particle:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed


def sum_position(particles):
    total = 0
    for particle in particles:
        total = total + particle.position
    return total


def sum_speed(particles):
    total = 0
    for particle in particles:
        total = total + particle.speed
    return total


def one_round(round_number):
    particles = []
    for index in range(10000):
        particles.append(Particle(index + round_number, index % 5))
    return sum_position(particles) + sum_speed(particles)


def all_rounds(rounds):
    total = 0
    for round_number in range(rounds):
        total = total + one_round(round_number)
    return total


def main():
    start = time.perf_counter_ns()
    total = all_rounds(200)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
