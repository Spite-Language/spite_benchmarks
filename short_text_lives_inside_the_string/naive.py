"""Makes lists of short labels like "r3 n41" and adds up their lengths and last characters, twenty rounds."""
import sys
import time


def make_labels(count, round):
    labels = []
    for index in range(count):
        labels.append("r%d n%d" % (round, index))
    return labels


def checksum(labels):
    total = 0
    for label in labels:
        last = len(label) - 1
        total = total + len(label) + ord(label[last])
    return total


def rounds(count):
    total = 0
    for round in range(count):
        labels = make_labels(100000, round)
        total = total + checksum(labels)
    return total


def main():
    start = time.perf_counter_ns()
    total = rounds(20)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
