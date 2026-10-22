"""One shared tally behind a lock, four threads that each call its add in a loop."""
# threading, as a Python programmer guards an object threads share: every call takes and lets go of the lock
import sys
import threading
import time


class Tally:
    def __init__(self):
        self.lock = threading.Lock()
        self.total = 0
        self.calls = 0
        self.largest = 0

    def add(self, amount):
        with self.lock:
            self.total = self.total + amount
            self.calls = self.calls + 1
            if amount > self.largest:
                self.largest = amount

    def sum(self):
        with self.lock:
            return self.total

    def call_count(self):
        with self.lock:
            return self.calls

    def largest_amount(self):
        with self.lock:
            return self.largest


class Counter:
    def __init__(self, tally, rounds):
        self.tally = tally
        self.rounds = rounds
        self.result = 0

    def count_up(self):
        for index in range(self.rounds):
            self.tally.add(index % 3)
        return self.rounds

    def run(self):
        self.result = self.count_up()


def count_on_four(tally, rounds):
    counters = [Counter(tally, rounds) for _ in range(4)]
    threads = [threading.Thread(target=counter.run) for counter in counters]
    for thread in threads:
        thread.start()
    counted = 0
    for thread, counter in zip(threads, counters):
        thread.join()
        counted = counted + counter.result
    return counted


def main():
    tally = Tally()
    start = time.perf_counter_ns()
    counted = count_on_four(tally, 5000000)
    total = tally.sum()
    calls = tally.call_count()
    largest = tally.largest_amount()
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"counted {counted} calls {calls} total {total} largest {largest}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
