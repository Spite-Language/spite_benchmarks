"""Runs sixty frames, each drawing and sleeping a millisecond, saving a part to a file (sleeping twenty milliseconds first) on each of the first eight."""
import os
import sys
import time


class Game:
    def __init__(self):
        self.next_part = 0
        self.saved = 0
        self.frames = 0
        self.checksum = 0

    def save_part(self):
        part = self.next_part
        self.next_part = self.next_part + 1
        time.sleep(0.020)
        with open(f".spite/frame_save_{part}.txt", "wb") as file:
            file.write(f"part {part}".encode())
        self.saved = self.saved + 1

    def draw(self):
        checksum = self.checksum
        frames = self.frames
        for index in range(20000):
            checksum = checksum + index * frames % 1000
        self.checksum = checksum


def main():
    os.makedirs(".spite", exist_ok=True)
    game = Game()
    start = time.perf_counter_ns()
    while game.frames < 60:
        game.frames = game.frames + 1
        game.draw()
        if game.frames <= 8:
            game.save_part()
        time.sleep(0.001)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"frames {game.frames} parts saved {game.saved} checksum {game.checksum}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
