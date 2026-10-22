"""Builds a text of ten thousand words by appending a piece at a time, for 8 rounds, and adds up the lengths."""
import sys
import time


def words(count):
    text = ""
    piece = "word "
    for index in range(count):
        text = text + piece
    return text


def main():
    start = time.perf_counter_ns()
    total = 0
    for round_number in range(8):
        text = words(10000)
        total = total + len(text)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"characters {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
