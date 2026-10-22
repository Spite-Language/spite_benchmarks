"""Notes ten million amounts in a ledger while a worker thread (threading) sums on its own."""
import sys
import threading
import time


class Ledger:
    def __init__(self):
        self.total = 0
        self.notes = 0
        self.milestones = []

    def note(self, amount):
        self.total = self.total + amount
        self.notes = self.notes + 1
        if amount % 1000000 == 0:
            self.milestones.append(amount)
        return amount + 1


class Worker:
    def __init__(self):
        self.result = 0

    def run(self):
        total = 0
        for index in range(1000):
            total = total + index % 7
        self.result = total


ledger = Ledger()


def ledger_is_large(amount):
    return amount > 10


def count_on_the_pool():
    worker = Worker()
    thread = threading.Thread(target=worker.run)
    thread.start()
    thread.join()
    return worker.result


def note_many(count):
    seen = 0
    index = 0
    while index < count:
        index = ledger.note(index)
        seen = seen + len(ledger.milestones)
    return seen


def main():
    start = time.perf_counter_ns()
    counted = count_on_the_pool()
    large = 0
    for amount in [4, 12, 30, 7]:
        large = large + ledger_is_large(amount)
    seen = note_many(10000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"counted {counted} large {large} seen {seen} notes {ledger.notes} "
          f"milestones {len(ledger.milestones)} total {ledger.total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
