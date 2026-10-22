"""Adds to a lock-guarded tally from one threading.Thread, then ten million times from the main thread."""
import sys
import threading
import time


class Tally:
    def __init__(self):
        self.lock = threading.Lock()
        self.total = 0
        self.calls = 0

    def add(self, amount):
        with self.lock:
            self.total = self.total + amount
            self.calls = self.calls + 1
        return amount + 1

    def sum(self):
        with self.lock:
            return self.total

    def call_count(self):
        with self.lock:
            return self.calls


class Worker:
    def __init__(self, tally):
        self.tally = tally
        self.result = 0

    def thread_main(self):
        self.result = self.tally.add(1)


def add_on_the_pool(tally):
    worker = Worker(tally)
    thread = threading.Thread(target=worker.thread_main)
    thread.start()
    thread.join()
    return worker.result


def add_many(tally, count):
    index = 0
    while index < count:
        index = tally.add(index)
    return index


def main():
    tally = Tally()
    start = time.perf_counter_ns()
    first = add_on_the_pool(tally)
    reached = add_many(tally, 10000000)
    total = tally.sum()
    calls = tally.call_count()
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"first {first} reached {reached} calls {calls} total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
