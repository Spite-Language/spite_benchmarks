"""An archive of letters and a gallery of paintings, each sorted 2000 times into a fresh list, one after the other."""
import sys
import time


class Item:
    def __init__(self, value):
        self.count = 1
        self.value = value


class Collection:
    def __init__(self, sort, factor):
        self.sort = sort
        self.items = [Item(index * factor % 1000) for index in range(2000)]
        self.total = 0


def keep(kept, item):
    item.count = item.count + 1
    kept.append(item)


def let_go(kept):
    for item in kept:
        item.count = item.count - 1


def archive_sort(collection):
    for round in range(2000):
        kept = []
        for letter in collection.items:
            if letter.value % 3 == round % 3:
                keep(kept, letter)
        collection.total = collection.total + len(kept)
        let_go(kept)


def gallery_sort(collection):
    for round in range(2000):
        hung = []
        for painting in collection.items:
            if painting.value % 5 == round % 5:
                keep(hung, painting)
        collection.total = collection.total + len(hung)
        let_go(hung)


def main():
    collections = [Collection(archive_sort, 7), Collection(gallery_sort, 11)]
    start = time.perf_counter_ns()
    for collection in collections:
        collection.sort(collection)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"{collections[0].total} {collections[1].total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
