"""One event log behind a lock, four threads that each record a quarter of a million entries."""
# threading, as in the C: every call takes and lets go of the lock around its append
import sys
import threading
import time


class EventLog:
    def __init__(self):
        self.lock = threading.Lock()
        self.entries = []

    def record(self, entry):
        with self.lock:
            self.entries.append(entry)

    def count(self):
        with self.lock:
            return len(self.entries)


class Logger:
    def __init__(self, log, rounds, source):
        self.log = log
        self.rounds = rounds
        self.source = source
        self.result = 0

    def entry_for(self, index):
        return self.source * 1000000 + index

    def log_all(self):
        for index in range(self.rounds):
            entry = self.entry_for(index)
            self.log.record(entry)
        return self.rounds

    def run(self):
        self.result = self.log_all()


def log_on_four(log, rounds):
    loggers = [Logger(log, rounds, index + 1) for index in range(4)]
    threads = [threading.Thread(target=logger.run) for logger in loggers]
    for thread in threads:
        thread.start()
    logged = 0
    for thread, logger in zip(threads, loggers):
        thread.join()
        logged = logged + logger.result
    return logged


def main():
    log = EventLog()
    start = time.perf_counter_ns()
    logged = log_on_four(log, 250000)
    count = log.count()
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"logged {logged} entries {count}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
