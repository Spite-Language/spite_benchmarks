"""Sums index % 7 over the even and odd numbers below 20 million, the evens on a thread of its own (the GIL makes it no faster)."""
import sys
import threading
import time


class Summer:
    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset
        self.result = 0

    def total(self):
        total = 0
        for index in range(self.offset, self.limit, 2):
            total = total + index % 7
        return total

    def run(self):
        self.result = self.total()


def sum_on_two(limit):
    evens = Summer(limit, 0)
    thread = threading.Thread(target=evens.run)
    thread.start()
    odds = Summer(limit, 1)
    odd_sum = odds.total()
    thread.join()
    return evens.result + odd_sum


def main():
    start = time.perf_counter_ns()
    total = sum_on_two(20000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
