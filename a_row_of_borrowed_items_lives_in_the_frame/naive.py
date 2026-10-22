"""Moves and heals 100000 entities for 100 ticks, each system called with a row object made for the call."""
import sys
import time


class Position:
    def __init__(self, left, top):
        self.left = left
        self.top = top


class Velocity:
    def __init__(self, across, down):
        self.across = across
        self.down = down


class Health:
    def __init__(self, amount):
        self.amount = amount


class Regeneration:
    def __init__(self, per_tick):
        self.per_tick = per_tick


class Moving:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


class Mending:
    def __init__(self, health, regeneration):
        self.health = health
        self.regeneration = regeneration


def mover_update_each(moving):
    moving.position.left = moving.position.left + moving.velocity.across
    moving.position.top = moving.position.top + moving.velocity.down


def healer_update_each(mending):
    mending.health.amount = mending.health.amount + mending.regeneration.per_tick


def spawn_all(count, positions, velocities, healths, regenerations):
    for entity in range(count):
        positions.append(Position(0, 0))
        velocities.append(Velocity(entity % 13 - 6, entity % 7 - 3))
        healths.append(Health(0))
        regenerations.append(Regeneration(entity % 4))


def tick_once(positions, velocities, healths, regenerations):
    for entity in range(len(positions)):
        if entity >= len(velocities) or entity >= len(healths) or entity >= len(regenerations):
            raise SystemExit(1)
        moving = Moving(positions[entity], velocities[entity])
        mover_update_each(moving)
        mending = Mending(healths[entity], regenerations[entity])
        healer_update_each(mending)


def run_ticks(count, positions, velocities, healths, regenerations):
    for tick in range(count):
        tick_once(positions, velocities, healths, regenerations)


def main():
    positions = []
    velocities = []
    healths = []
    regenerations = []
    start = time.perf_counter_ns()
    spawn_all(100000, positions, velocities, healths, regenerations)
    run_ticks(100, positions, velocities, healths, regenerations)
    places = 0
    for position in positions:
        places = places + (position.left + position.top)
    amounts = 0
    for health in healths:
        amounts = amounts + health.amount
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"places {places} health {amounts}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
