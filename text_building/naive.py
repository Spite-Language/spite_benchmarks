"""Builds one long text of "item <n>," pieces and one comma-joined text of "word<n>" words."""
import sys
import time


def main():
    start = time.perf_counter_ns()
    pieces = []
    for index in range(3000000):
        pieces.append("item ")
        pieces.append(str(index))
        pieces.append(",")
    built = "".join(pieces)
    words = []
    for index in range(1000000):
        words.append("word" + str(index))
    joined = ", ".join(words)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"built {len(built)} joined {len(joined)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
