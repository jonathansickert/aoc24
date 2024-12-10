from copy import deepcopy

from aoc24.aoc_decorator import isinbound, solves_puzzle, to_str_grid

step_lookup: dict[str, tuple[int, int, str]] = {
    "^": (-1, 0, ">"),
    ">": (0, 1, "V"),
    "V": (1, 0, "<"),
    "<": (0, -1, "^"),
}


def find_start(grid: list[str]) -> tuple[int, int, str]:
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (dir := grid[x][y]) in {"^", ">", "V", "<"}:
                return x, y, dir
    raise Exception


def place_obstacle_ahead(
    x: int, y: int, dir: str, grid: list[str]
) -> tuple[int, int] | None:
    dx, dy, _ = step_lookup[dir]
    ox, oy = x + dx, y + dy
    if not isinbound(ox, oy, grid) or grid[ox][oy] != ".":
        return None
    grid[ox] = grid[ox][:oy] + "#" + grid[ox][oy + 1 :]
    return ox, oy


def simulate_run(
    start_x: int, start_y: int, start_dir: str, grid: list[str]
) -> tuple[bool, set[tuple[int, int, str]]]:
    path = set()
    x, y, dir = start_x, start_y, start_dir

    while True:
        if (x, y, dir) in path:
            return False, path  # loop
        path.add((x, y, dir))
        dx, dy, new_dir = step_lookup[dir]
        new_x, new_y = x + dx, y + dy
        if not isinbound(new_x, new_y, grid):
            return True, path  # exit
        if grid[new_x][new_y] == "#":
            dir = new_dir
        else:
            x, y = new_x, new_y


@solves_puzzle(day=6)
def solve_both_parts(input: str) -> tuple[int, int]:
    grid: list[str] = to_str_grid(input)
    start_x, start_y, start_dir = find_start(grid)
    _, path = simulate_run(start_x, start_y, start_dir, grid)
    loop_obstacle_positions = set()
    for step in path:
        new_grid: list[str] = deepcopy(grid)
        if (pos := place_obstacle_ahead(*step, new_grid)) is not None:
            success, _ = simulate_run(start_x, start_y, start_dir, new_grid)
            if success is False:
                loop_obstacle_positions.add(pos)
    return len({(step[0], step[1]) for step in path}), len(loop_obstacle_positions)


if __name__ == "__main__":
    solve_both_parts()
