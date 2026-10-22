"""Two columns of components, velocities and trails, integrated and summed for 100 ticks."""
import sys
import time


class Velocity:
    def __init__(self, across, down):
        self.across = across
        self.down = down

    def integrate(self):
        self.across = self.across + self.down


class Trail:
    def __init__(self, across, down):
        self.across = across
        self.down = down
        self.marks = []

    def integrate(self):
        self.across = self.across + self.down


def fill(velocities, trails, count):
    for index in range(count):
        velocities.append(Velocity(index % 100, index % 7))
        trails.append(Trail(index % 50, index % 5))


def ticks(velocities, trails):
    total = 0
    for tick in range(100):
        for velocity in velocities:
            velocity.integrate()
        for trail in trails:
            trail.integrate()
        moved = 0
        for velocity in velocities:
            moved = moved + velocity.across
        trailed = 0
        for trail in trails:
            trailed = trailed + trail.across
        total = total + moved + trailed
    return total


def main():
    start = time.perf_counter_ns()
    velocities = []
    trails = []
    fill(velocities, trails, 100000)
    total = ticks(velocities, trails)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
