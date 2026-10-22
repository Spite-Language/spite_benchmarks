"""Build 999000 sentences by joining a name, a phrase, the next name and another phrase, one join at a time."""
import sys
import time


def meetings(names):
    total = 0
    for index in range(len(names) - 1):
        first = names[index] + " meets "
        second = first + names[index + 1]
        line = second + " at the gate."
        total = total + len(line)
    return total


def main():
    start = time.perf_counter_ns()
    names = []
    for index in range(1000):
        names.append(f"traveller number {index}")
    total = 0
    for round in range(1000):
        total = total + meetings(names)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"characters {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
