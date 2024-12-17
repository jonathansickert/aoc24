import heapq
import sys

from aoc24.aoc_decorator import solves_puzzle


def get_min_dist(
    dist: dict[tuple[int, int], int], queue: set[tuple[int, int]]
) -> tuple[int, int]:
    # min_dist: int = min(v for k, v in dist.items() if k in queue)
    min_dist = float("inf")
    min_v: tuple[int, int]
    for v in queue:
        if dist[v] < min_dist:
            min_v = v
            min_dist = dist[v]
    return min_v

    # for k, v in dist.items():
    #     if v == min_dist and k in queue:
    #         return k
    # raise Exception("No min found!")


def get_new_dist(cur_dx: int, cur_dy: int, dx: int, dy: int) -> int:
    x_diff: int = abs(cur_dx - dx)
    y_diff: int = abs(cur_dy - dy)
    return max(x_diff, y_diff) * 1000


def dijkstra(V: set[tuple[int, int]], S: tuple[int, int]):
    dist: dict[tuple[int, int], int] = {}
    prev: dict[tuple[int, int], list[tuple[int, int]]] = {}
    dir: dict[tuple[int, int], tuple[int, int]] = {}

    for v in V:
        dist[v] = sys.maxsize
        prev[v] = []
    dist[S] = 0
    dir[S] = (0, 1)

    Q = []
    heapq.heappush(Q, (0, S))

    while Q:
        du, u = heapq.heappop(Q)
        dx, dy = dir[u]

        if du > dist[u]:
            continue

        for ndx, ndy in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
            n = (u[0] + ndx, u[1] + ndy)
            if n in V:
                new_dist: int = du + get_new_dist(dx, dy, ndx, ndy) + 1
                if new_dist < dist[n]:
                    dist[n] = new_dist
                    dir[n] = (ndx, ndy)
                    heapq.heappush(Q, (new_dist, n))
                    prev[n] = [u]
                elif new_dist == dist[n]:
                    prev[n].append(u)
                    # print("equal: ", prev[n])
        # print()
    return dist, prev


# def dijkstra2(V: set[tuple[int, int]], S: tuple[int, int], E):
#     dist: dict[tuple[int, int], int] = {}
#     prev = {}
#     dir: dict[tuple[int, int], tuple[int, int]] = {S: (0, 1)}
#     Q = set()
#     for v in V:
#         dist[v] = float("inf")
#         prev[v] = []
#         Q.add(v)
#     dist[S] = 0
#     prev[v] = None

#     while len(Q) > 0:
#         u = get_min_dist(dist, Q)
#         Q.remove(u)
#         dx, dy = dir[u]
#         for ndx, ndy in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
#             n = (u[0] + ndx, u[1] + ndy)
#             if n in V:
#                 new_dist: int = dist[u] + get_new_dist(dx, dy, ndx, ndy) + 1
#                 if new_dist <= dist[n]:
#                     dist[n] = new_dist
#                     dir[n] = (ndx, ndy)
#                     prev[n].append(u)
#                     print(prev[n])
#     return prev


# def dijkstra(V: set[tuple[int, int]], S: tuple[int, int]) -> dict[tuple[int, int], int]:
#     dist: dict[tuple[int, int], int] = {}
#     prev: dict[tuple[int, int], tuple[int, int] | None] = {}
#     dir: dict[tuple[int, int], tuple[int, int]] = {S: (0, 1)}
#     queue: set[tuple[int, int]] = set()
#     for v in V:
#         dist[v] = float("inf")
#         prev[v] = None
#         queue.add(v)
#         # heapq.heappush(Q, (float("inf"), v))
#     dist[S] = 0

#     while len(queue) > 0:
#         u = get_min_dist(dist, queue)
#         queue.remove(u)
#         # _, u = heapq.heappop(Q)
#         # print(u)
#         dx, dy = dir[u]
#         for ndx, ndy in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
#             if (n := (u[0] + ndx, u[1] + ndy)) in queue:
#                 new_dist: int = dist[u] + get_new_dist(dx, dy, ndx, ndy) + 1
#                 # new_dist: int = dist[u] + 1
#                 if new_dist < dist[n]:
#                     dist[n] = new_dist
#                     prev[n] = u
#                     dir[n] = (ndx, ndy)
#                     # heapq.heapreplace()
#     return dist


def path_length(
    prev: dict[tuple[int, int], list[tuple[int, int]]],
    E: tuple[int, int],
) -> int:
    visited = []

    def walk_path_recursive(cur: tuple[int, int]):
        prevs = prev.get(cur)
        # print()
        if prevs is None or len(prevs) == 0:
            return
        for p in prevs:
            visited.append(p)
            walk_path_recursive(p)

    walk_path_recursive(E)
    return len(visited)


def walk_path(E: tuple[int, int], prev: dict[tuple[int, int], tuple[int, int]]):
    path = []
    cur: tuple[int, int] = E
    while 1:
        path.insert(0, cur)
        next = prev.get(cur)
        if next is None:
            break
        cur = next
    return path


@solves_puzzle(day=16, part=1)
def solve_part_1(input: str):
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
    # print(len(V))
    dist, prev = dijkstra(V, S)
    # print(path_length(prev, E))
    # prevs_len = {k: len(v) for k, v in prev.items() if len(v) > 1}
    # print(prevs_len)
    # for x in range(len(grid)):
    #     for y in range(len(grid[0])):
    #         if (x, y) in path:
    #             print("X", end="")
    #         else:
    #             print(grid[x][y], end="")
    #     print()

    return dist[E]


if __name__ == "__main__":
    # for dx, dy in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
    #     print(dx, dy)
    #     print(get_new_dist(-1, 0, dx, dy))

    solve_part_1()
