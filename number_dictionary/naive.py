"""Fills a dictionary keyed by numbers, then looks up many keys, counting those found and summing their values."""
import sys
import time


def main():
    start = time.perf_counter_ns()
    scores = {}
    for index in range(500000):
        scores[index * 7] = index
    total = 0
    found = 0
    for round_number in range(10):
        for index in range(500000):
            score = scores.get(index * 3)
            if score is not None:
                total = total + score
                found = found + 1
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"entries {len(scores)} found {found} total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
