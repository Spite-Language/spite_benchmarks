"""Groups 200000 orders into 32768 fresh bucket lists, forty times, and adds up the largest bucket of each round."""
import sys
import time


class Order:
    def __init__(self, customer):
        self.customer = customer


def group(orders, round):
    buckets = []
    for _ in range(32768):
        buckets.append([])
    for order in orders:
        buckets[(order.customer + round) % 32768].append(order)
    return buckets


def largest(buckets):
    most = 0
    for bucket in buckets:
        if len(bucket) > most:
            most = len(bucket)
    return most


def main():
    orders = []
    seed = 777
    for _ in range(200000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        orders.append(Order(seed % 32768))
    start = time.perf_counter_ns()
    total = 0
    for round in range(40):
        buckets = group(orders, round)
        total += largest(buckets)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
