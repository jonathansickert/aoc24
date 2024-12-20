import heapq
from collections import defaultdict
from typing import Iterator

from aoc24.aoc_decorator import solves_puzzle

Cheat = tuple[int, int, int, int, int, int]


def isinbound(x: int, y: int, grid: list[str]) -> bool:
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def find_race_cheats(grid: list[str]) -> Iterator[Cheat]:
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "#":  # start cannot be wall
                continue
            for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                nx1, ny1 = x + dx, y + dy
                nx2, ny2 = x + 2 * dx, y + 2 * dy

                if (
                    isinbound(nx1, ny1, grid)
                    and isinbound(nx2, ny2, grid)
                    and grid[nx1][ny1] == "#"
                    and grid[nx2][ny2] == "."
                ):
                    yield x, y, nx1, ny1, nx2, ny2


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


@solves_puzzle(day=20, part=1)
def solve_part_1(input: str) -> int:
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

    for cheat in set(find_race_cheats(grid)):
        sx, sy, wx, wy, ex, ey = cheat
        dist_to_cheat_start: float = dists_from_S[(sx, sy)]
        dist_fro_cheat_end: float = dists_from_E[(ex, ey)]
        total_dist_using_cheat: float = dist_to_cheat_start + 2 + dist_fro_cheat_end
        if total_dist_using_cheat < dist_E:
            answer1 += 1 if dist_E - total_dist_using_cheat >= 100 else 0

    return answer1


if __name__ == "__main__":
    solve_part_1()
