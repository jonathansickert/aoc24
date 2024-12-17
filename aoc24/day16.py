import heapq
import sys
from collections import defaultdict
from typing import TypeAlias

from aoc24.aoc_decorator import solves_puzzle

State: TypeAlias = tuple[int, int, int]


def neighbours(cur_x, cur_y, cur_d):
    yield 1000, (cur_x, cur_y, (cur_d + 1) % 4)
    yield 1000, (cur_x, cur_y, (cur_d - 1) % 4)
    dx, dy = [(0, 1), (1, 0), (0, -1), (-1, 0)][cur_d]
    yield 1, (cur_x + dx, cur_y + dy, cur_d)


def dijkstra(
    V: set[tuple[int, int]], S: tuple[int, int]
) -> tuple[dict[State, int], dict[State, set[State]]]:
    dist: dict[State, int] = defaultdict(lambda: sys.maxsize)
    prev: dict[State, set[State]] = defaultdict(lambda: set())
    s: State = (*S, 0)
    dist[s] = 0
    Q = []
    heapq.heappush(Q, (0, s))

    while Q:
        cur_cost, cur = heapq.heappop(Q)
        cur_x, cur_y, cur_d = cur

        if cur_cost > dist[cur]:
            continue

        for cost, v in neighbours(cur_x, cur_y, cur_d):
            vx, vy, vd = v
            if (vx, vy) in V:
                v_cost: int = cur_cost + cost
                if v_cost < dist[v]:
                    dist[v] = v_cost
                    heapq.heappush(Q, (v_cost, v))
                    prev[v].add(cur)
                elif v_cost <= dist[v]:
                    prev[v].add(cur)
    return dist, prev


def bfs(E: State, prevs: dict[State, set[State]]) -> int:
    visited = set()
    visited.add(E)
    Q: list[State] = [E]
    while Q:
        cur: State = Q.pop()
        for prev in prevs[cur]:
            visited.add(prev)
            Q.append(prev)
    return len({(x, y) for x, y, _ in visited})


@solves_puzzle(day=16)
def solve_both_parts(input: str) -> tuple[int, int]:
    grid: list[str] = input.splitlines()
    V = set()
    S: tuple[int, int] = (-1, -1)
    E: tuple[int, int] = (-1, -1)
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == ".":
                V.add((x, y))
            if grid[x][y] == "S":
                S = (x, y)
                V.add(S)
            if grid[x][y] == "E":
                E = (x, y)
                V.add(E)
    dist, prev = dijkstra(V, S)
    answer1: int = min(dist[(E[0], E[1], i)] for i in range(4))
    answer2: int = min(bfs((E[0], E[1], i), prev) for i in range(4))
    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
