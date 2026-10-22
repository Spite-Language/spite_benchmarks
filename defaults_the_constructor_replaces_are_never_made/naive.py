"""Makes 50000 items per round, each built with a default owner its constructor replaces, and sums prices and ages."""
import sys
import time


class Owner:
    def __init__(self, age):
        self.age = age


class Item:
    def __init__(self, price, owner):
        self.price = 0
        self.owner = Owner(0)
        self.price = price
        self.owner = owner


def map_owners(items):
    owners = []
    for item in items:
        owners.append(item.owner)
    return owners


def sum_age(owners):
    total = 0
    for owner in owners:
        total = total + owner.age
    return total


def sum_price(items):
    total = 0
    for item in items:
        total = total + item.price
    return total


def one_round(round_number):
    items = []
    for index in range(50000):
        owner = Owner((index + round_number) % 90)
        items.append(Item(index % 1000, owner))
    owners = map_owners(items)
    ages = sum_age(owners)
    return sum_price(items) + ages


def all_rounds(rounds):
    total = 0
    for round_number in range(rounds):
        total = total + one_round(round_number)
    return total


def main():
    start = time.perf_counter_ns()
    total = all_rounds(10)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
