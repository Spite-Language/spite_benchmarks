"""Prices ten million amounts through a pipeline of steps, testing each step against every kind of step."""
import sys
import time

STEP_DISCOUNT, STEP_TAX, STEP_ROUNDING, STEP_COUPON = 0, 1, 2, 3


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


def main():
    start = time.perf_counter_ns()
    checkout = Pipeline()
    checkout.add(STEP_DISCOUNT)
    checkout.add(STEP_TAX)
    checkout.add(STEP_DISCOUNT)
    total = 0
    for index in range(10000000):
        amount = 1000 + index % 1000
        total = total + checkout.price(amount)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
