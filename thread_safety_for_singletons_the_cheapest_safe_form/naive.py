"""Four threading.Threads hit a lock-guarded counter and read lock-guarded settings; a plain journal is kept by the main thread."""
import sys
import threading
import time


class HitCounter:
    def __init__(self):
        self.lock = threading.Lock()
        self.hits = 0

    def record(self, amount):
        with self.lock:
            self.hits = self.hits + amount

    def total(self):
        with self.lock:
            return self.hits


class Settings:
    def __init__(self, step, label):
        self.lock = threading.Lock()
        self.step = step
        self.label = label

    def step_size(self):
        with self.lock:
            return self.step

    def name(self):
        with self.lock:
            return self.label


class Journal:
    def __init__(self):
        self.lines = []

    def note(self, line):
        self.lines.append(line)

    def written(self):
        return len(self.lines)


class Worker:
    def __init__(self, counter, settings, rounds):
        self.counter = counter
        self.settings = settings
        self.rounds = rounds
        self.result = 0

    def run(self):
        index = 0
        while index < self.rounds:
            step = self.settings.step_size()
            self.counter.record(step)
            index = index + 1
        return index

    def thread_main(self):
        self.result = self.run()


def count_on_four(counter, settings, rounds):
    workers = []
    threads = []
    for _ in range(4):
        worker = Worker(counter, settings, rounds)
        thread = threading.Thread(target=worker.thread_main)
        workers.append(worker)
        threads.append(thread)
        thread.start()
    total = 0
    for worker, thread in zip(workers, threads):
        thread.join()
        total = total + worker.result
    return total


def main():
    counter = HitCounter()
    settings = Settings(2, "hits")
    journal = Journal()
    start = time.perf_counter_ns()
    journal.note("starting")
    rounds = count_on_four(counter, settings, 1000000)
    journal.note("finished")
    name = settings.name()
    total = counter.total()
    written = journal.written()
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"{name} {total} after {rounds} rounds, journal lines: {written}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
