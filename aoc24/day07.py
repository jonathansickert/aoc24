from aoc24.aoc_decorator import solves_puzzle, to_str_grid


def has_combination(
    numbers: list[int], target: int, support_concat: bool = False
) -> bool:
    def _has_combination(numbers: list[int], acc: int, target: int) -> bool:
        if len(numbers) == 0:
            return acc == target
        if acc > target:
            return False
        cur: int = numbers[0]
        return (
            _has_combination(numbers[1:], acc + cur, target)
            or _has_combination(numbers[1:], acc * cur, target)
            or (
                _has_combination(numbers[1:], int(str(acc) + str(cur)), target)
                if support_concat is True
                else False
            )
        )

    return _has_combination(numbers[1:], numbers[0], target)


@solves_puzzle(day=7)
def solve_both_parts(input: str) -> tuple[int, int]:
    lines_split: list[list[str]] = [line.split(":") for line in to_str_grid(input)]
    equations: dict[int, list[int]] = {
        int(line[0]): list(map(int, line[1].split())) for line in lines_split
    }
    answer1: int = 0
    answer2: int = 0
    for target, numbers in equations.items():
        if has_combination(numbers=numbers, target=target):
            answer1 += target
        if has_combination(numbers, target, support_concat=True):
            answer2 += target
    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
