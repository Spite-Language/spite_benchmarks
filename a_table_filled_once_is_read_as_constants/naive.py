"""Prices 10 million amounts through a checkout whose steps are a list of codes filled once."""
import sys
import time

STEP_DISCOUNT = 0
STEP_TAX = 1
STEP_ROUNDING = 2
STEP_COUPON = 3


class Pipeline:
    def __init__(self):
        self.steps = []

    def add(self, step):
        self.steps.append(step)

    def price(self, amount):
        total = amount
        for step in self.steps:
            if step == STEP_DISCOUNT:
                total = total - total // 10
            if step == STEP_TAX:
                total = total + total // 5
            if step == STEP_ROUNDING:
                total = total // 100 * 100
            if step == STEP_COUPON:
                total = total - 50
        return total


def checkout_make():
    checkout = Pipeline()
    checkout.add(STEP_DISCOUNT)
    checkout.add(STEP_TAX)
    checkout.add(STEP_DISCOUNT)
    return checkout


def main():
    start = time.perf_counter_ns()
    checkout = checkout_make()
    total = 0
    for index in range(10000000):
        amount = 1000 + index % 1000
        total = total + checkout.price(amount)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
