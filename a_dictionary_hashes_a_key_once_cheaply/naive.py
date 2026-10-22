"""Index 5000 names in a dictionary and look them up 2000000 times, each lookup written twice."""
import sys
import time


def make_names(count):
    names = []
    for index in range(count):
        names.append(f"entity_{index}")
    return names


def index_names(names):
    by_name = {}
    for index in range(len(names)):
        by_name[names[index]] = index * 3
    return by_name


def look_up(names, by_name):
    total = 0
    for round in range(20):
        for index in range(100000):
            position = (index * 7 + round) % 5000
            name = names[position]
            if by_name.get(name) is not None:
                total = total + by_name.get(name)
    return total


def main():
    start = time.perf_counter_ns()
    names = make_names(5000)
    by_name = index_names(names)
    total = look_up(names, by_name)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total} entries {len(by_name)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
