from copy import deepcopy

from aoc24.input import read_input_lines

input: list[str] = read_input_lines(day=6)
grid: list[str] = (
    ["@" * (len(input[0]) + 2)]
    + ["@" + line + "@" for line in input]
    + ["@" * (len(input[0]) + 2)]
)
step_lookup: dict[str, tuple[int, int, str]] = {
    "^": (-1, 0, ">"),
    ">": (0, 1, "V"),
    "V": (1, 0, "<"),
    "<": (0, -1, "^"),
}
answer_1: int = 0
answer_2: int = 0


def walk(x: int, y: int, facing: str, grid: list[str]) -> tuple[int, int, str] | None:
    dx, dy, new_facing = step_lookup[facing]
    obstacle: str = grid[x + dx][y + dy]
    if obstacle == "@":  # end of the map
        return None
    if obstacle == "#":  # facing an obstacle
        return x, y, new_facing
    if obstacle == ".":  # facing no obstacle
        return x + dx, y + dy, facing


def find_start(grid: list[str]) -> tuple[int, int]:
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "^":
                grid[x] = grid[x][:y] + "." + grid[x][y + 1 :]
                return x, y
    return (-1, -1)


def is_loop(start_x: int, start_y: int, facing: str, grid: list[str]) -> bool:
    steps: set = set()
    cur_x, cur_y, cur_facing = start_x, start_y, facing
    while 1:
        steps.add((cur_x, cur_y, cur_facing))
        new_step = walk(cur_x, cur_y, cur_facing, grid)
        if new_step is None:
            break
        cur_x, cur_y, cur_facing = new_step
        if (cur_x, cur_y, cur_facing) in steps:
            return True  # detected loop
    return False


def place_obstacle_ahead(
    cur_x: int, cur_y: int, facing: str, grid: list[str]
) -> tuple[int, int] | None:
    dx, dy, _ = step_lookup[facing]
    x, y = cur_x + dx, cur_y + dy
    if grid[x][y] == ".":
        grid[x] = grid[x][:y] + "#" + grid[x][y + 1 :]
        return x, y
    return None


def run(start_x: int, start_y: int, grid: list[str]) -> tuple[int, int]:
    steps: set = set()
    loop_obstacles: set = set()
    cur_x, cur_y = start_x, start_y
    cur_facing: str = "^"
    while 1:
        steps.add((cur_x, cur_y))
        test_grid: list[str] = deepcopy(grid)
        new_obstacle = place_obstacle_ahead(cur_x, cur_y, cur_facing, test_grid)
        if new_obstacle is not None:
            if is_loop(start_x, start_y, "^", test_grid) is True:
                loop_obstacles.add(new_obstacle)
        new_step = walk(cur_x, cur_y, cur_facing, grid)
        if new_step is None:
            break
        cur_x, cur_y, cur_facing = new_step
    return len(steps), len(loop_obstacles)


start_x, start_y = find_start(grid)
answer_1, answer_2 = run(start_x, start_y, grid)

print(answer_1)
print(answer_2)
