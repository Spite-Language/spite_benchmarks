"""Writes a notes file and reads it back for 50 rounds, then removes it (plain blocking calls, no threads)."""
import os
import sys
import time


def file_write(path, text):
    with open(path, "wb") as file:
        return file.write(text) == len(text)


def file_read(path):
    with open(path, "rb") as file:
        return file.read()


def write_and_read(path, rounds):
    characters = 0
    for round_number in range(rounds):
        text = f"round {round_number} of the notes".encode()
        file_write(path, text)
        read = file_read(path)
        characters = characters + len(read)
    return characters


def main():
    os.makedirs(".spite", exist_ok=True)
    path = ".spite/concurrency_machinery_notes.txt"
    start = time.perf_counter_ns()
    characters = write_and_read(path, 50)
    os.remove(path)
    removed = True
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"characters {characters} removed {'true' if removed else 'false'}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
