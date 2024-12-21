import heapq
from collections import defaultdict
from typing import Iterator

from aoc24.aoc_decorator import solves_puzzle

Cheat = tuple[int, int, int, int, int]


def isinbound(x: int, y: int, grid: list[str]) -> bool:
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def find_cheats_of_length(x: int, y: int, length: int, grid: list[str]) -> set[Cheat]:
    cheats: set[Cheat] = set()

    for dx in range(1, length + 1):
        for dy in range(1, length + 1 - dx):
            for mx, my in {(1, 1), (1, -1), (-1, -1), (-1, 1)}:
                nx: int = x + mx * dx
                ny: int = y + my * dy
                if isinbound(nx, ny, grid) and grid[nx][ny] == ".":
                    cheats.add((x, y, nx, ny, dx + dy))

    for d in range(1, length + 1):
        for mx, my in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
            nx: int = x + mx * d
            ny: int = y + my * d
            if isinbound(nx, ny, grid) and grid[nx][ny] == ".":
                cheats.add((x, y, nx, ny, d))

    return cheats


def neighbours(x: int, y: int, grid: list[str]) -> Iterator[tuple[int, int]]:
    for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
        nx, ny = x + dx, y + dy
        if isinbound(nx, ny, grid) and grid[nx][ny] == ".":
            yield nx, ny


def dijkstra(
    S: tuple[int, int], grid: list[str]
) -> defaultdict[tuple[int, int], float]:
    dists: dict[tuple[int, int], float] = defaultdict(lambda: float("inf"))
    dists[S] = 0
    Q = []
    heapq.heapify(Q)
    heapq.heappush(Q, (0, S))

    while Q:
        d, cur = heapq.heappop(Q)
        x, y = cur

        for n in neighbours(x, y, grid):
            nd = d + 1
            if nd < dists[n]:
                dists[n] = float(nd)
                heapq.heappush(Q, (nd, n))

    return dists


@solves_puzzle(day=20)
def solve_both_parts(input: str) -> tuple[int, int]:
    grid: list[str] = input.splitlines()

    S: tuple[int, int]
    E: tuple[int, int]

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "S":
                S = x, y
                grid[x] = grid[x][:y] + "." + grid[x][y + 1 :]
            if grid[x][y] == "E":
                E = x, y
                grid[x] = grid[x][:y] + "." + grid[x][y + 1 :]

    assert S, "no start (S) found"
    assert E, "no end (E) found"

    dists_from_S: defaultdict[tuple[int, int], float] = dijkstra(S, grid)
    dists_from_E: defaultdict[tuple[int, int], float] = dijkstra(E, grid)
    dist_E: float = dists_from_S[E]
    assert dist_E.is_integer(), "end (E) unreachable"

    answer1: int = 0
    answer2: int = 0

    cheats = set()

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == ".":
                cheats.update(find_cheats_of_length(x, y, 20, grid))

    for cheat in cheats:
        sx, sy, ex, ey, length = cheat
        dist_to_cheat_start: float = dists_from_S[(sx, sy)]
        dist_fro_cheat_end: float = dists_from_E[(ex, ey)]
        total_dist_using_cheat: float = (
            dist_to_cheat_start + length + dist_fro_cheat_end
        )
        if total_dist_using_cheat < dist_E:
            answer1 += (
                1 if dist_E - total_dist_using_cheat >= 100 and length == 2 else 0
            )
            answer2 += 1 if dist_E - total_dist_using_cheat >= 100 else 0

    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
