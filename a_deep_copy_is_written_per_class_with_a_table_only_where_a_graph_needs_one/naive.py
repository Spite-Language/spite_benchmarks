"""Deep-copies a list of orders with a copy function per class, forty times, and sums their values."""
import sys
import time


class Customer:
    def __init__(self, name, level):
        self.name = name
        self.level = level


class Line:
    def __init__(self, quantity, price):
        self.quantity = quantity
        self.price = price


class Order:
    def __init__(self, id, customer):
        self.id = id
        self.customer = customer
        self.lines = []


def customer_deep_copy(customer):
    return Customer(customer.name, customer.level)


def line_deep_copy(line):
    return Line(line.quantity, line.price)


def lines_deep_copy(lines):
    copied = []
    for line in lines:
        copied.append(line_deep_copy(line))
    return copied


def order_deep_copy(order):
    copied = Order(order.id, customer_deep_copy(order.customer))
    copied.lines = lines_deep_copy(order.lines)
    return copied


def orders_deep_copy(orders):
    copied = []
    for order in orders:
        copied.append(order_deep_copy(order))
    return copied


def line_amount(line):
    return line.quantity * line.price


def order_value(order):
    amount = 0
    for line in order.lines:
        amount += line_amount(line)
    return amount + order.customer.level + order.id % 3


def add_lines(order, index):
    for line_index in range(4):
        order.lines.append(Line(line_index + 1, index % 97 + line_index))


def make_orders(count):
    orders = []
    for index in range(count):
        customer = Customer("customer %d" % (index % 300), index % 5)
        order = Order(index, customer)
        add_lines(order, index)
        orders.append(order)
    return orders


def copy_rounds(orders):
    total = 0
    for _ in range(40):
        copies = orders_deep_copy(orders)
        copies[0].id += 3
        value = 0
        for copy in copies:
            value += order_value(copy)
        total += value
    return total


def main():
    start = time.perf_counter_ns()
    orders = make_orders(5000)
    total = copy_rounds(orders)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
