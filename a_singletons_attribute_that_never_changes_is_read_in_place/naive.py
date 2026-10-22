"""Fill a shelf of boxes, then read every box through the shelf's lock from a second thread."""
# threading: the reader runs on a thread of its own, the shelf is behind a lock, as in the C
import sys
import threading
import time


class Box:
    def __init__(self, weight):
        self.weight = weight


class Shelf:
    def __init__(self):
        self.lock = threading.Lock()
        self.boxes = []

    def insert(self, box):
        with self.lock:
            self.boxes.append(box)

    def count(self):
        with self.lock:
            return len(self.boxes)

    def box_at(self, place):
        with self.lock:
            if 0 <= place < len(self.boxes):
                return self.boxes[place]
            return None


class Reader:
    def __init__(self, shelf, rounds):
        self.shelf = shelf
        self.rounds = rounds
        self.result = 0

    def read_round(self, rows, round):
        total = 0
        for row in range(rows):
            place = (row * 7 + round) % rows
            box = self.shelf.box_at(place)
            if box is None:
                print(f"no box at {place}", file=sys.stderr)
                sys.exit(1)
            total = total + box.weight
        return total

    def run(self):
        rows = self.shelf.count()
        total = 0
        for round in range(self.rounds):
            total = total + self.read_round(rows, round)
        self.result = total


def fill_shelf(shelf, count):
    for index in range(count):
        shelf.insert(Box(index % 100))


def read_on_the_pool(shelf):
    reader = Reader(shelf, 4)
    thread = threading.Thread(target=reader.run)
    thread.start()
    thread.join()
    return reader.result


def main():
    shelf = Shelf()
    start = time.perf_counter_ns()
    fill_shelf(shelf, 1000000)
    total = read_on_the_pool(shelf)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
