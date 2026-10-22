"""Adds up picked values from a list for 300 rounds, each pick checked against the list with its crash report written where the check is."""
import sys
import time


def round_total(values, picks, round_number):
    total = 0
    for index in range(len(picks)):
        pick = picks[index] + round_number
        if pick < 0 or pick >= len(values):
            sys.stdout.flush()
            sys.stderr.write(
                "crash naive.spite:39 in Naive.round_total\tvalues[pick] is missing: index %d, count %d\tround=%d\ttotal=%d\tindex=%d\n"
                % (pick, len(values), round_number, total, index))
            sys.exit(1)
        total = total + values[pick]
    return total


def picked_total(values, picks):
    total = 0
    for round_number in range(300):
        total = total + round_total(values, picks, round_number)
    return total


def main():
    start = time.perf_counter_ns()
    values = []
    for index in range(1300):
        values.append(index * 7 % 1000)
    picks = []
    for index in range(100000):
        picks.append(index * 13 % 1000)
    total = picked_total(values, picks)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
