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


def dijkstra(V: set[tuple[int, int]], S: tuple[int, int]) -> dict[tuple[int, int], int]:
    dist: dict[tuple[int, int], int] = {}
    prev: dict[tuple[int, int], tuple[int, int] | None] = {}
    dir: dict[tuple[int, int], tuple[int, int]] = {S: (0, 1)}
    queue: set[tuple[int, int]] = set()
    for v in V:
        dist[v] = float("inf")
        prev[v] = None
        queue.add(v)
        # heapq.heappush(Q, (float("inf"), v))
    dist[S] = 0

    while len(queue) > 0:
        u = get_min_dist(dist, queue)
        queue.remove(u)
        # _, u = heapq.heappop(Q)
        # print(u)
        dx, dy = dir[u]
        for ndx, ndy in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
            if (n := (u[0] + ndx, u[1] + ndy)) in queue:
                new_dist: int = dist[u] + get_new_dist(dx, dy, ndx, ndy) + 1
                # new_dist: int = dist[u] + 1
                if new_dist < dist[n]:
                    dist[n] = new_dist
                    prev[n] = u
                    dir[n] = (ndx, ndy)
                    # heapq.heapreplace()
    return dist


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
    dist: dict[tuple[int, int], int] = dijkstra(V, S)
    return dist[E]


if __name__ == "__main__":
    # for dx, dy in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
    #     print(dx, dy)
    #     print(get_new_dist(-1, 0, dx, dy))

    solve_part_1()
