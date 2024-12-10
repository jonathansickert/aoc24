from itertools import permutations
from typing import Iterator

from aoc24.aoc_decorator import isinbound, solves_puzzle, to_str_grid


def find_antinode(
    ax: int, ay: int, bx: int, by: int, grid: list[str]
) -> Iterator[tuple[int, int]]:
    if isinbound(x := 2 * ax - bx, y := 2 * ay - by, grid):
        yield x, y


def find_antinodes(
    ax: int, ay: int, bx: int, by: int, grid: list[str]
) -> Iterator[tuple[int, int]]:
    while isinbound(ax, ay, grid) and isinbound(bx, by, grid):
        yield ax, ay
        ax, ay, bx, by = 2 * ax - bx, 2 * ay - by, ax, ay


@solves_puzzle(day=8)
def solve_both_parts(input: str) -> tuple[int, int]:
    grid: list[str] = to_str_grid(input)
    antennas: dict[str, list[tuple[int, int]]] = {}
    visited1 = set()
    visited2 = set()
    for row, line in enumerate(grid):
        for col, symbol in enumerate(line):
            if symbol != ".":
                antennas.setdefault(symbol, []).append((row, col))

    for points in antennas.values():
        for a, b in permutations(points, 2):
            visited1.update(find_antinode(*a, *b, grid))
            visited2.update(find_antinodes(*a, *b, grid))
    return len(visited1), len(visited2)


if __name__ == "__main__":
    solve_both_parts()
