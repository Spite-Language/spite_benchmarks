"""Matches three million entities against column headers, passing a list of rows down two calls (run on a threading.Thread, as naive.c does)."""
import sys
import threading
import time


class Matcher:
    def __init__(self, column_count):
        self.headers = []
        for index in range(column_count):
            self.headers.append(index + 1)

    def find_row(self, index, entity, found):
        if index < 0 or index >= len(self.headers):
            print("no header %d" % index, file=sys.stderr)
            sys.exit(1)
        place = entity % self.headers[index]
        found[index] = place
        return place >= 0

    def match_into(self, entity, found):
        index = 0
        everything = True
        while everything and index < len(self.headers):
            everything = self.find_row(index, entity, found)
            index = index + 1
        return everything


class Stream:
    def __init__(self, entity_count):
        self.entity_count = entity_count
        self.result = 0

    def run_positions(self, matcher, rows):
        total = 0
        for entity in range(self.entity_count):
            if matcher.match_into(entity, rows):
                total = total + rows[2]
        return total

    def run(self):
        matcher = Matcher(3)
        found = [0, 0, 0]
        return self.run_positions(matcher, found)

    def thread_main(self):
        self.result = self.run()


def stream_on_the_pool(entity_count):
    stream = Stream(entity_count)
    thread = threading.Thread(target=stream.thread_main)
    thread.start()
    thread.join()
    return stream.result


def main():
    start = time.perf_counter_ns()
    total = stream_on_the_pool(3000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
