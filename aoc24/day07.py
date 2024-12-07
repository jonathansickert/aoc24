from aoc24.input import read_input_lines

lines: list[str] = read_input_lines(day=7)
lines_split: list[list[str]] = [line.split(":") for line in lines]
equations: dict[int, list[int]] = {
    int(line[0]): list(map(int, line[1].split())) for line in lines_split
}
answer_1: int = 0
answer_2: int = 0


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


for target, numbers in equations.items():
    if has_combination(numbers=numbers, target=target):
        answer_1 += target
    if has_combination(numbers, target, support_concat=True):
        answer_2 += target

print(answer_1)
print(answer_2)
