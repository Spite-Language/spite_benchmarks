"""Probes a list of entries at scattered places, counting where an entry is found, then sums the keys."""
import sys
import time


class Entry:
    def __init__(self, key):
        self.key = key


def list_get(items, index):
    if 0 <= index < len(items):
        return items[index]
    return None


def probe(entries, probes):
    found = 0
    missing = 0
    at = 0
    for index in range(probes):
        at = (at + 7919) % 400000
        if list_get(entries, at) is not None:
            found = found + 1
        else:
            missing = missing + 1
    if found + missing != probes:
        raise SystemExit(1)
    return found


def sum_key(entries):
    total = 0
    for entry in entries:
        total = total + entry.key
    return total


def main():
    start = time.perf_counter_ns()
    entries = []
    for index in range(200000):
        entries.append(Entry(index % 1000))
    found = probe(entries, 20000000)
    keys = sum_key(entries)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"found {found} keys {keys}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
