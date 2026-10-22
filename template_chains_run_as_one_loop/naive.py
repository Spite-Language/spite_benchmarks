"""Filters, maps and sums a list of items and their owners in chains, each step making its own list."""
import sys
import time


class Owner:
    def __init__(self, age):
        self.age = age

    def is_adult(self):
        return self.age >= 18


class Item:
    def __init__(self, price, active, owner):
        self.price = price
        self.active = active
        self.owner = owner

    def is_active(self):
        return self.active


def totals(items):
    total = 0
    for round_number in range(100):
        active = [item for item in items if item.is_active()]
        prices = sum(item.price for item in active)
        active_again = [item for item in items if item.is_active()]
        owners = [item.owner for item in active_again]
        adults = [owner for owner in owners if owner.is_adult()]
        ages = sum(owner.age for owner in adults)
        total = total + prices + ages
    return total


def main():
    start = time.perf_counter_ns()
    items = []
    for index in range(100000):
        owner = Owner(index % 90)
        items.append(Item(index % 1000, index % 3 != 0, owner))
    total = totals(items)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
