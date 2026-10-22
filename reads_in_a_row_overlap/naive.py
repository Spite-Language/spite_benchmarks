"""Writes two text files once, then reads both of them in each of 40 rounds and counts their characters."""
import os
import sys
import time


def make_text(word, count):
    text = ""
    for index in range(count):
        if index == 0:
            text = text + f"{word} line number {index}"
        else:
            text = text + f"\n{word} line number {index}"
    return text


def file_write(path, text):
    with open(path, "wb") as file:
        return file.write(text) == len(text)


def file_read(path):
    with open(path, "rb") as file:
        return file.read()


def read_both(first_path, second_path):
    first = file_read(first_path)
    second = file_read(second_path)
    return len(first) + len(second)


def read_rounds(first_path, second_path, rounds):
    characters = 0
    for round_number in range(rounds):
        characters = characters + read_both(first_path, second_path)
    return characters


def main():
    os.makedirs(".spite", exist_ok=True)
    first_path = ".spite/reads_in_a_row_first.txt"
    second_path = ".spite/reads_in_a_row_second.txt"
    first_text = make_text("first", 4000).encode()
    second_text = make_text("second", 4000).encode()
    file_write(first_path, first_text)
    file_write(second_path, second_text)
    start = time.perf_counter_ns()
    characters = read_rounds(first_path, second_path, 40)
    microseconds = (time.perf_counter_ns() - start) // 1000
    os.remove(first_path)
    os.remove(second_path)
    print(f"characters {characters} removed true true")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
