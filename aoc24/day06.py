from copy import deepcopy

from aoc24.input import read_input_lines

input: list[str] = read_input_lines(day=6)
step_lookup: dict[str, tuple[int, int, str]] = {
    "^": (-1, 0, ">"),
    ">": (0, 1, "V"),
    "V": (1, 0, "<"),
    "<": (0, -1, "^"),
}
answer_1: int = 0
answer_2: int = 0


def isinbound(x: int, y: int, grid: list[str]) -> bool:
    return x < len(grid) and x >= 0 and y < len(grid[0]) and y >= 0


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


start_x, start_y, start_dir = find_start(input)
_, path = simulate_run(start_x, start_y, start_dir, input)
loop_obstacle_positions = set()
for step in path:
    new_grid: list[str] = deepcopy(input)
    if (pos := place_obstacle_ahead(*step, new_grid)) is not None:
        success, _ = simulate_run(start_x, start_y, start_dir, new_grid)
        if success is False:
            loop_obstacle_positions.add(pos)

answer_1 = len({(step[0], step[1]) for step in path})
answer_2 = len(loop_obstacle_positions)

print(answer_1)
print(answer_2)
