"""Steps a list of particles two hundred times, storing each changed particle back into its slot."""
import sys
import time


class Particle:
    def __init__(self, starting_speed):
        self.left = 0
        self.speed = starting_speed


def step(particles):
    for index in range(len(particles)):
        particle = particles[index]
        particle.left = particle.left + particle.speed
        particles[index] = particle


def sum_left(particles):
    total = 0
    for particle in particles:
        total = total + particle.left
    return total


def main():
    start = time.perf_counter_ns()
    particles = []
    for index in range(200000):
        particles.append(Particle(index % 7 + 1))
    for _ in range(200):
        step(particles)
    total = sum_left(particles)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
