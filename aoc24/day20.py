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


# def find_cheat_ends(x: int, y: int, l: int, grid: list[str]):


def neighbours(x: int, y: int, grid: list[str]) -> Iterator[tuple[int, int]]:
    for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
        nx, ny = x + dx, y + dy
        if isinbound(nx, ny, grid) and grid[nx][ny] == ".":
            yield nx, ny


def dijkstra(
    S: tuple[int, int], E: tuple[int, int], cheat: Cheat | None, grid: list[str]
) -> int:
    dist: dict[tuple[int, int], float] = defaultdict(lambda: float("inf"))
    dist[S] = 0
    Q = []
    heapq.heapify(Q)
    heapq.heappush(Q, (0, S))

    while Q:
        d, cur = heapq.heappop(Q)
        x, y = cur

        if cheat and cheat[0] == x and cheat[1] == y:  # wa can take the cheat
            n = cheat[4], cheat[5]
            nd = d + 2
            if nd < dist[n]:
                dist[n] = nd
                heapq.heappush(Q, (nd, n))
            else:  # cheat did not help
                return -1

        for n in neighbours(x, y, grid):
            nd = d + 1
            if nd < dist[n]:
                dist[n] = nd
                heapq.heappush(Q, (nd, n))

    assert dist[E] != float("inf"), "end (E) could not be reached"
    return int(dist[E])
    # return dist


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

    distance: int = dijkstra(S, E, None, grid)
    cheats = set(find_race_cheats(grid))

    print(distance)
    print(len(cheats))

    # return 0

    # cheat_dists = defaultdict(int)

    answer1: int = 0
    for cheat in cheats:
        cheat_distance: int = dijkstra(S, E, cheat, grid)
        if cheat_distance == -1:
            continue
        distance_diff: int = distance - cheat_distance
        if distance_diff >= 100:
            # cheat_dists[distance_diff] += 1
            answer1 += 1

    # print(cheat_dists)

    return answer1


if __name__ == "__main__":
    solve_part_1()
