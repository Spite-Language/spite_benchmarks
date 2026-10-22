"""Makes sale records (--records=N, default 2000000), then sums units, profit per region and quarter, and fingerprints."""
import sys
import time


class Sale:
    def __init__(self, seed):
        self.region = seed % 16
        self.product = seed // 16 % 1000
        self.quantity = seed // 16000 % 20 + 1
        self.price = seed // 320000 % 500 + 100
        self.cost = self.price * 3 // 4 - seed % 37
        self.discount = seed % 101
        self.day = seed // 7 % 365
        self.customer = seed // 2555 % 100000


def fingerprint(sale):
    total = sale.region
    total = total + sale.product * 3 + sale.quantity * 5 + sale.price * 7 + sale.cost * 11
    total = total + sale.discount * 13 + sale.day * 17 + sale.customer * 19
    return total


def profit_of(sales, region, quarter):
    profit = 0
    for sale in sales:
        if sale.region == region and sale.day // 92 == quarter:
            profit = profit + sale.quantity * (sale.price - sale.cost)
    return profit


def records_of(arguments, otherwise):
    for argument in arguments:
        if argument.startswith("--records="):
            return int(argument[10:])
    return otherwise


def main():
    records = records_of(sys.argv[1:], 2000000)
    start = time.perf_counter_ns()
    sales = []
    seed = 42
    for index in range(records):
        seed = seed * 48271 % 2147483647
        sales.append(Sale(seed))
    made = time.perf_counter_ns()
    units = 0
    for sale in sales:
        units = units + sale.quantity
    summed = time.perf_counter_ns()
    by_cell = 0
    for cell in range(64):
        by_cell = by_cell + profit_of(sales, cell // 4, cell % 4) * (cell + 1)
    profited = time.perf_counter_ns()
    fingerprints = 0
    for sale in sales:
        fingerprints = fingerprints + fingerprint(sale)
    finished = time.perf_counter_ns()
    print(f"units {units} by region and quarter {by_cell} fingerprints {fingerprints} first {sales[0].customer}")
    print(f"microseconds {(finished - start) // 1000}", file=sys.stderr)
    print(f"phases make {(made - start) // 1000} one {(summed - made) // 1000} "
          f"five {(profited - summed) // 1000} all {(finished - profited) // 1000}", file=sys.stderr)


if __name__ == "__main__":
    main()
