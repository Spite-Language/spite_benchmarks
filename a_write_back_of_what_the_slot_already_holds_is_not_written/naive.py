"""A desk of pages: take one into the open page, add a word, put it back into its slot, 100 rounds."""
import sys
import time


class Page:
    def __init__(self, words):
        self.words = words


class Desk:
    def __init__(self):
        self.pages = []
        self.open = None
        self.at = 0

    def stock(self, count):
        for index in range(count):
            self.pages.append(Page(index % 7))

    def take(self, index):
        self.at = index
        if self.at < 0 or self.at >= len(self.pages):
            raise IndexError(self.at)
        self.open = self.pages[self.at]

    def put_back(self):
        if self.at < 0 or self.at >= len(self.pages):
            raise IndexError(self.at)
        self.pages[self.at] = self.open


def main():
    desk = Desk()
    desk.stock(100000)
    start = time.perf_counter_ns()
    for round in range(100):
        for index in range(100000):
            desk.take(index)
            desk.open.words = desk.open.words + 1
            desk.put_back()
    total = 0
    for page in desk.pages:
        total = total + page.words
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"words {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
