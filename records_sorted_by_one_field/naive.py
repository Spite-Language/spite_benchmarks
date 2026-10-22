"""Makes orders, sorts a copy of them by the time they were placed, then walks them for a running total and an audit sum."""
import sys
import time


class Order:
    def __init__(self, id, placed_at, customer, product, quantity, price, region, status):
        self.id = id
        self.placed_at = placed_at
        self.customer = customer
        self.product = product
        self.quantity = quantity
        self.price = price
        self.region = region
        self.status = status


def make_order(id, seed):
    return Order(id, seed, seed // 3 % 50000, seed // 7 % 2000, seed % 9 + 1, seed // 11 % 500 + 100,
                 seed % 16, seed // 13 % 4)


def audit(order):
    total = order.customer
    return total + order.product * 3 + order.region * 5 + order.status * 7


def setting_of(arguments, flag, otherwise):
    for argument in arguments[1:]:
        if argument.startswith(flag):
            return int(argument[len(flag):])
    return otherwise


def main():
    count = setting_of(sys.argv, "--orders=", 2000000)
    start = time.perf_counter_ns()
    orders = []
    seed = 3
    for index in range(count):
        seed = seed * 48271 % 2147483647
        orders.append(make_order(index, seed))
    made = time.perf_counter_ns()
    by_time = list(orders)
    by_time.sort(key=lambda order: order.placed_at)
    sorted_at = time.perf_counter_ns()
    running = 0
    for order in by_time:
        running = (running * 31 + order.quantity * order.price) % 1000000007
    audits = 0
    for order in by_time:
        audits = audits + audit(order)
    finished = time.perf_counter_ns()
    print(f"running {running} audits {audits} first {by_time[0].id} last {by_time[-1].id}")
    print(f"microseconds {(finished - start) // 1000}", file=sys.stderr)
    print(f"phases make {(made - start) // 1000} sort {(sorted_at - made) // 1000} walk {(finished - sorted_at) // 1000}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
