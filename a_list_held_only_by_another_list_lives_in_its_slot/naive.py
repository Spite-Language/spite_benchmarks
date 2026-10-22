"""Groups orders into one list per customer and asks the total amount of customers' buckets, ten rounds."""
import sys
import time


class Order:
    def __init__(self, customer, amount):
        self.customer = customer
        self.amount = amount


def make_orders(count):
    orders = []
    seed = 12345
    for index in range(count):
        seed = (seed * 1103515245 + 12345) % 2147483648
        orders.append(Order(seed % 65536, seed % 1000))
    return orders


def group(orders):
    buckets = []
    for made in range(65536):
        buckets.append([])
    for order in orders:
        buckets[order.customer].append(order)
    return buckets


def ask(buckets, round_number):
    asked = 0
    customer = round_number
    for query in range(400000):
        customer = (customer * 7919 + 13) % 65536
        bucket = buckets[customer]
        for at in range(len(bucket)):
            asked += bucket[at].amount
    return asked


def main():
    orders = make_orders(400000)
    start = time.perf_counter_ns()
    total = 0
    for round_number in range(10):
        buckets = group(orders)
        total += ask(buckets, round_number)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
