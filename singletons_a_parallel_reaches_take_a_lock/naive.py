"""One shared registry behind a lock, four threads that each record a weight 250000 times."""
# threading, as in the C: every call takes and lets go of the lock around its append and its addition
import sys
import threading
import time


class Registry:
    def __init__(self):
        self.lock = threading.Lock()
        self.weights = []
        self.total = 0

    def record(self, weight):
        with self.lock:
            self.weights.append(weight)
            self.total = self.total + weight

    def recorded(self):
        with self.lock:
            return len(self.weights)

    def sum(self):
        with self.lock:
            return self.total


class Recorder:
    def __init__(self, registry, rounds):
        self.registry = registry
        self.rounds = rounds
        self.result = 0

    def weight_of(self, index):
        return index % 10 + 1

    def record_all(self):
        for index in range(self.rounds):
            weight = self.weight_of(index)
            self.registry.record(weight)
        return self.rounds

    def run(self):
        self.result = self.record_all()


def record_on_four(registry, rounds):
    recorders = [Recorder(registry, rounds) for _ in range(4)]
    threads = [threading.Thread(target=recorder.run) for recorder in recorders]
    for thread in threads:
        thread.start()
    counted = 0
    for thread, recorder in zip(threads, recorders):
        thread.join()
        counted = counted + recorder.result
    return counted


def main():
    registry = Registry()
    start = time.perf_counter_ns()
    counted = record_on_four(registry, 250000)
    recorded = registry.recorded()
    total = registry.sum()
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"counted {counted} recorded {recorded} total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
