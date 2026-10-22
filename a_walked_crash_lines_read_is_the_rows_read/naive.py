"""Runs a mover system over entities held in sparse-set columns, finding each row's components through lists."""
import sys
import time


class Entity:
    def __init__(self, id):
        self.id = id


class Position:
    def __init__(self, left, top):
        self.left = left
        self.top = top


class Velocity:
    def __init__(self, across, down):
        self.across = across
        self.down = down


class SparseSet:
    def __init__(self):
        self.dense_of = []
        self.entities = []

    def place(self, entity):
        while len(self.dense_of) <= entity:
            self.dense_of.append(0)
        self.entities.append(entity)
        self.dense_of[entity] = len(self.entities)

    def dense_index(self, entity):
        if entity >= len(self.dense_of):
            return -1
        return self.dense_of[entity] - 1


class Column:
    def __init__(self):
        self.set = SparseSet()
        self.values = []

    def insert(self, entity, value):
        self.set.place(entity)
        self.values.append(value)

    def at(self, index):
        if index < 0 or index >= len(self.values):
            return None
        return self.values[index]


class Moving:
    def __init__(self, entity, position, velocity):
        self.entity = entity
        self.position = position
        self.velocity = velocity


state = {"marked": 0, "missing": 0, "positions": None, "velocities": None}


def position_column():
    if state["positions"] is None:
        state["positions"] = Column()
    return state["positions"]


def velocity_column():
    if state["velocities"] is None:
        state["velocities"] = Column()
    return state["velocities"]


def mover_update_each(moving):
    moving.position.left = moving.position.left + moving.velocity.across
    moving.position.top = moving.position.top + moving.velocity.down
    if moving.entity.id % 1000 == 0:
        state["marked"] = state["marked"] + 1


def list_at(items, index):
    if index < 0 or index >= len(items):
        return None
    return items[index]


def note(found, dense):
    if dense < 0:
        state["missing"] = 1
    found.append(dense)


def run(found, entity_count):
    for entity in range(entity_count):
        found.clear()
        state["missing"] = 0
        note(found, entity)
        note(found, position_column().set.dense_index(entity))
        note(found, velocity_column().set.dense_index(entity))
        if not state["missing"]:
            made = Entity(entity)
            if list_at(found, 1) is None:
                raise SystemExit(1)
            position_row = list_at(found, 1)
            if position_column().at(position_row) is None:
                raise SystemExit(1)
            position = position_column().at(position_row)
            if list_at(found, 2) is None:
                raise SystemExit(1)
            velocity_row = list_at(found, 2)
            if velocity_column().at(velocity_row) is None:
                raise SystemExit(1)
            velocity = velocity_column().at(velocity_row)
            mover_update_each(Moving(made, position, velocity))


def main():
    start = time.perf_counter_ns()
    entity_count = 100000
    for entity in range(entity_count):
        position_column().insert(entity, Position(0, 0))
    for backwards in range(entity_count - 1, -1, -1):
        if backwards % 3 != 0:
            velocity_column().insert(backwards, Velocity(backwards % 13 - 6, backwards % 7 - 3))
    found = []
    for tick in range(50):
        run(found, entity_count)
    places = 0
    for position in position_column().values:
        places = places + (position.left + position.top)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"places {places} marked {state['marked']}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
