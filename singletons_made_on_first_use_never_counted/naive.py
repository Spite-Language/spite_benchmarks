"""Two threads each make ten million visits that fetch the one shared Rules, made by the first to ask behind a lock (threading; Python counts references itself, so no counter is kept)."""
import sys
import threading
import time


class Rules:
    def __init__(self):
        self.base = 3


rules_lock = threading.Lock()
rules_made = None


def rules_get():
    global rules_made
    with rules_lock:
        if rules_made is None:
            rules_made = Rules()
        return rules_made


class Visit:
    def __init__(self, number):
        self.rules = rules_get()
        self.number = number

    def weight(self):
        return self.number % 7 + self.rules.base


class Fetcher:
    def __init__(self, rounds):
        self.rounds = rounds
        self.result = 0

    def fetch_many(self):
        found = 0
        for index in range(self.rounds):
            visit = Visit(index)
            found = found + visit.weight()
        self.result = found


def fetch_on_two(rounds):
    fetchers = []
    threads = []
    for index in range(2):
        fetcher = Fetcher(rounds)
        thread = threading.Thread(target=fetcher.fetch_many)
        fetchers.append(fetcher)
        threads.append(thread)
        thread.start()
    fetched = 0
    for index in range(2):
        threads[index].join()
        fetched = fetched + fetchers[index].result
    return fetched


def main():
    start = time.perf_counter_ns()
    fetched = fetch_on_two(10000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"fetched {fetched}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
