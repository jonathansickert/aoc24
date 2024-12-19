import heapq
from typing import Iterator

from aoc24.aoc_decorator import solves_puzzle

INF = float("inf")


def isinbound(x: int, y: int, grid: list[list[int]]) -> bool:
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def neighbours(x: int, y: int, grid: list[list[int]]) -> Iterator[tuple[int, int]]:
    for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
        nx, ny = x + dx, y + dy
        if isinbound(nx, ny, grid) and grid[nx][ny] == 0:
            yield nx, ny


def parse_input(input: str) -> list[tuple[int, int]]:
    nums: list[tuple[int, ...]] = [
        tuple(map(int, line.split(","))) for line in input.splitlines()
    ]
    return [(x, y) for x, y in nums]


def generate_grid(grid_size: int) -> list[list[int]]:
    return [[0] * grid_size for _ in range(grid_size)]


def dijkstra(grid: list[list[int]], S: tuple[int, int], E: tuple[int, int]) -> int:
    dist: dict[tuple[int, int], float] = {}
    Q = []
    heapq.heapify(Q)
    heapq.heappush(Q, (0, S))

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0:
                dist[(x, y)] = INF

    while Q:
        d, cur = heapq.heappop(Q)
        x, y = cur
        for n in neighbours(x, y, grid):
            nd = d + 1
            if nd < dist[n]:
                dist[n] = nd
                heapq.heappush(Q, (nd, n))

    if dist.get(E) is not None:
        return int(dist[E]) if dist[E] < INF else -1
    return -1


@solves_puzzle(day=18, part=1)
def solve_part_1(input: str) -> int:
    falling_bytes: list[tuple[int, int]] = parse_input(input)
    grid: list[list[int]] = generate_grid(grid_size=71)
    for y, x in falling_bytes[:1024]:
        grid[x][y] = 1
    return dijkstra(grid, (0, 0), (70, 70))


@solves_puzzle(day=18, part=2)
def solve_part_2(input: str) -> int:
    falling_bytes: list[tuple[int, int]] = parse_input(input)

    def is_blocked(cur: int) -> bool:
        grid: list[list[int]] = generate_grid(grid_size=71)
        for y, x in falling_bytes[:cur]:
            grid[x][y] = 1
        if dijkstra(grid, (0, 0), (70, 70)) == -1:
            return True
        return False

    left: int = 0
    right: int = len(falling_bytes) - 1

    while left <= right:
        cur: int = left + (right - left) // 2

        if not is_blocked(cur):
            left = cur + 1
            continue

        if is_blocked(cur) and not is_blocked(cur - 1):
            y, x = falling_bytes[cur - 1]
            print(f"{y},{x}")
            return 0

        right = cur - 1

    raise ValueError("no solution")


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
