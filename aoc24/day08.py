from itertools import permutations
from typing import Iterator

from aoc24.input import read_input_lines

lines: list[str] = read_input_lines(day=8)
antennas: dict[str, list[tuple[int, int]]] = {}
visited_1 = set()
visited_2 = set()
answer_1: int = 0
answer_2: int = 0

for row, line in enumerate(lines):
    for col, symbol in enumerate(line):
        if symbol != ".":
            antennas.setdefault(symbol, []).append((row, col))


def isinbound(x: int, y: int) -> bool:
    return x < len(lines) and x >= 0 and y < len(lines[0]) and y >= 0


def find_antinode(ax: int, ay: int, bx: int, by: int) -> Iterator[tuple[int, int]]:
    if isinbound(x := 2 * ax - bx, y := 2 * ay - by):
        yield x, y


def find_antinodes(ax: int, ay: int, bx: int, by: int) -> Iterator[tuple[int, int]]:
    while isinbound(ax, ay) and isinbound(bx, by):
        yield ax, ay
        ax, ay, bx, by = 2 * ax - bx, 2 * ay - by, ax, ay


for points in antennas.values():
    for a, b in permutations(points, 2):
        visited_1.update(find_antinode(*a, *b))
        visited_2.update(find_antinodes(*a, *b))

answer_1 = len(visited_1)
answer_2 = len(visited_2)

print(answer_1)
print(answer_2)
