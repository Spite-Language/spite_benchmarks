"""Fills lists of velocities and entity numbers 40 times and removes the despawned ones from each in one walk that moves the kept down."""
import sys
import time

ITEM_TOTAL = 200000


class Velocity:
    def __init__(self, entity, despawned):
        self.entity = entity
        self.despawned = despawned


class World:
    def __init__(self):
        self.velocities = []
        self.entities = []
        self.marks = []

    def mark_every(self, total, removed_in_ten):
        self.marks = []
        for entity in range(total):
            scattered = entity * 7 % 10
            self.marks.append(scattered < removed_in_ten)

    def marked(self, entity):
        if entity >= len(self.marks):
            sys.stdout.flush()
            sys.stderr.write(f"no mark for entity {entity}\n")
            sys.exit(1)
        return self.marks[entity]

    def fill(self):
        self.velocities = []
        self.entities = []
        for entity in range(ITEM_TOTAL):
            despawned_now = self.marked(entity)
            self.velocities.append(Velocity(entity, despawned_now))
            self.entities.append(entity)

    def kept_sum(self):
        total = 0
        for row in range(len(self.velocities)):
            total = total + self.velocities[row].entity + self.entities[row]
        return total


def remove_despawned(items):
    kept = 0
    for index in range(len(items)):
        if not items[index].despawned:
            items[kept] = items[index]
            kept += 1
    del items[kept:]


def remove_where(items, test):
    kept = 0
    for index in range(len(items)):
        if not test(items[index]):
            items[kept] = items[index]
            kept += 1
    del items[kept:]


def main():
    world = World()
    start = time.perf_counter_ns()
    checksum = 0
    for round_number in range(40):
        removed_in_ten = 9 if round_number % 2 == 1 else 5
        world.mark_every(ITEM_TOTAL, removed_in_ten)
        world.fill()
        remove_despawned(world.velocities)
        remove_where(world.entities, world.marked)
        checksum = checksum + world.kept_sum()
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"checksum {checksum}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
