"""A spreadsheet of cells: twenty rounds of an edit and a recalculation of every cell, then the sum of placements."""
import sys
import time

CONSTANT, SUM, PRODUCT, SCALED = 0, 1, 2, 3


class Cell:
    def __init__(self, index, seed):
        self.formula = CONSTANT
        self.first = 0
        self.second = 0
        self.constant = seed % 1000
        self.value = 0
        self.row = index // 64
        self.column = index % 64
        self.style = seed % 5
        if index % 10 != 0:
            back = index - 1 - seed % 64
            self.first = back if back > 0 else 0
            self.second = seed // 64 % index
            choice = seed // 7 % 3
            self.formula = SUM if choice == 0 else PRODUCT if choice == 1 else SCALED


def computed(cell, left, right):
    if cell.formula == CONSTANT:
        return cell.constant
    if cell.formula == SUM:
        return (left + right) % 1000003
    if cell.formula == PRODUCT:
        return left * right % 1000003
    return left * cell.constant % 1000003


def recalculate(cells):
    for cell in cells:
        left = cells[cell.first].value
        right = cells[cell.second].value
        cell.value = computed(cell, left, right)


def setting_of(flag, otherwise):
    for argument in sys.argv[1:]:
        if argument.startswith(flag):
            return int(argument[len(flag):])
    return otherwise


def main():
    count = setting_of("--cells=", 1000000)
    start = time.perf_counter_ns()
    cells = []
    seed = 5
    for index in range(count):
        seed = seed * 48271 % 2147483647
        cells.append(Cell(index, seed))
    made = time.perf_counter_ns()
    total = 0
    for round in range(20):
        edited = round * 7919 % len(cells) // 10 * 10
        cells[edited].constant = round + 1
        recalculate(cells)
        values = 0
        for cell in cells:
            values = values + cell.value
        total = total + values
    recalculated = time.perf_counter_ns()
    placements = 0
    for cell in cells:
        placements = placements + cell.row * 64 + cell.column + cell.style * 100000000
    finished = time.perf_counter_ns()
    print(f"total {total} last {cells[-1].value} placements {placements}")
    print(f"microseconds {(finished - start) // 1000}", file=sys.stderr)
    print(f"phases make {(made - start) // 1000} recalculate {(recalculated - made) // 1000} place {(finished - recalculated) // 1000}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
