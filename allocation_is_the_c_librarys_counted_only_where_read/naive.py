"""Builds a linked chain of a thousand nodes per round, sums it, and drops it, for 2000 rounds."""
import sys
import time


class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next = next_node


def made_chain(length, round_number):
    head = Node(round_number, None)
    for index in range(1, length):
        added = Node(index + round_number, head)
        head = added
    return head


def chain_sum(head):
    total = 0
    current = head
    while current is not None:
        total = total + current.value
        current = current.next
    return total


def all_rounds(rounds):
    total = 0
    for round_number in range(rounds):
        chain = made_chain(1000, round_number)
        total = total + chain_sum(chain)
    return total


def main():
    start = time.perf_counter_ns()
    total = all_rounds(2000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
