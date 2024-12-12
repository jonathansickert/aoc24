from collections import deque

from aoc24.aoc_decorator import isinbound, solves_puzzle, to_str_grid

dirs = {(-1, 0), (0, 1), (1, 0), (0, -1)}


def find_region(start_x: int, start_y: int, grid: list[str]):
    region = set()
    q = deque([(start_x, start_y)])
    kind = grid[start_x][start_y]
    while q:
        x, y = q.pop()
        region.add((x, y))
        for dx, dy in dirs:
            if isinbound(x + dx, y + dy, grid) and grid[x + dx][y + dy] == kind:
                if (x + dx, y + dy) not in region:
                    region.add((x + dx, y + dy))
                    q.appendleft((x + dx, y + dy))
    return region


def find_perimeter(region: set[tuple[int, int]]) -> int:
    perimeter: int = 0
    for x, y in region:
        n_neighbuors: int = 0
        for dx, dy in dirs:
            if (x + dx, y + dy) in region:
                n_neighbuors += 1
        perimeter += 4 - n_neighbuors
    return perimeter


def find_n_sides(region: set[tuple[int, int]]) -> int:
    def sides_in_direction(dx: int, dy: int) -> int:
        neighbours = set()
        for x, y in region:
            if (x + dx, y + dy) not in region:
                neighbours.add((x + dx, y + dy))
        n_side_duplicates = 0
        for x, y in neighbours:
            if (x + abs(dy), y + abs(dx)) in neighbours:
                n_side_duplicates += 1
        return len(neighbours) - n_side_duplicates

    return sum(sides_in_direction(dx, dy) for dx, dy in dirs)


@solves_puzzle(day=12)
def solve_both_parts(input: str) -> tuple[int, int]:
    grid = to_str_grid(input)
    visited = set()
    answer1: int = 0
    answer2: int = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (x, y) in visited:
                continue
            region = find_region(x, y, grid)
            answer1 += find_perimeter(region) * len(region)
            answer2 += find_n_sides(region) * len(region)
            visited.update(region)
    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
