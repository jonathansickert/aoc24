from aoc24.aoc_decorator import solves_puzzle


def calculate_stone_length(stones: list[int], blinks: int):
    mem: dict[tuple[int, int], int] = {}

    def solve_recursive(stone: int, blinks: int):
        if blinks == 0:
            return 1
        if (stone, blinks) not in mem:
            if stone == 0:
                mem[(stone, blinks)] = solve_recursive(1, blinks - 1)
            elif (length := len(str(stone))) % 2 == 0:
                mem[((stone, blinks))] = solve_recursive(
                    int(str(stone)[: length // 2]), blinks - 1
                ) + solve_recursive(int(str(stone)[length // 2 :]), blinks - 1)
            else:
                mem[(stone, blinks)] = solve_recursive(stone * 2024, blinks - 1)
        return mem[((stone, blinks))]

    return sum(solve_recursive(stone, blinks) for stone in stones)


@solves_puzzle(day=11, part=1)
def solve_part_1(input: str) -> int:
    stones: list[int] = [int(stone) for stone in input.split()]
    return calculate_stone_length(stones, blinks=25)


@solves_puzzle(day=11, part=2)
def solve_part_2(input: str) -> int:
    stones: list[int] = [int(stone) for stone in input.split()]
    return calculate_stone_length(stones, blinks=75)


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
