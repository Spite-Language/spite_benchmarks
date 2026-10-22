"""Builds a line of text from pieces and two numbers a hundred thousand times per round, for 20 rounds, and adds up the line lengths."""
import sys
import time


def lines(count, round_number):
    total = 0
    for index in range(count):
        index_text = str(index)
        round_text = str(round_number)
        line = "".join(["line ", index_text, " of ", round_text, ";"])
        total = total + len(line)
    return total


def main():
    start = time.perf_counter_ns()
    total = 0
    for round_number in range(20):
        total = total + lines(100000, round_number)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"characters {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
