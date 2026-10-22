"""Scores medal results by building a three-entry dictionary on every call and reading its three keys."""
import sys
import time


class Result:
    def __init__(self, golds, silvers, bronzes):
        self.golds = golds
        self.silvers = silvers
        self.bronzes = bronzes


def points_for(result):
    points = {"gold": 50, "silver": 20, "bronze": 5}
    gold = points["gold"]
    silver = points["silver"]
    bronze = points["bronze"]
    return result.golds * gold + result.silvers * silver + result.bronzes * bronze


def totals(results):
    total = 0
    for round_number in range(40):
        for result in results:
            total = total + points_for(result)
    return total


def main():
    start = time.perf_counter_ns()
    results = []
    for index in range(200000):
        results.append(Result(index % 4, index % 7, index % 11))
    total = totals(results)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"points {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
