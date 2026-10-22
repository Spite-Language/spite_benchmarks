"""Total the attributes of 200000 stats objects 40 times, each read through a list of attribute objects."""
import sys
import time

CLASS_INTEGER = 1

STATS_ATTRIBUTES = [
    ("strength", CLASS_INTEGER),
    ("agility", CLASS_INTEGER),
    ("wisdom", CLASS_INTEGER),
    ("stamina", CLASS_INTEGER),
]


class Stats:
    def __init__(self, seed):
        self.strength = seed % 20
        self.agility = seed % 17
        self.wisdom = seed % 13
        self.stamina = seed % 11


class Attribute:
    def __init__(self, name, class_id, owner):
        self.name = name
        self.class_id = class_id
        self.owner = owner

    def value(self):
        return getattr(self.owner, self.name)


def attributes_of(stats):
    attributes = []
    for name, class_id in STATS_ATTRIBUTES:
        attributes.append(Attribute(name, class_id, stats))
    return attributes


def total_of(stats):
    running = 0
    for attribute in attributes_of(stats):
        if attribute.class_id == CLASS_INTEGER:
            running = running + attribute.value()
    return running


def party_total(party):
    total = 0
    for stats in party:
        total = total + total_of(stats)
    return total


def main():
    start = time.perf_counter_ns()
    party = [Stats(index) for index in range(200000)]
    total = 0
    for round in range(40):
        total = total + party_total(party)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
