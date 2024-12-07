from aoc24.input import read_input_lines

lines: list[str] = read_input_lines(day=2)
lines_split: list[list[str]] = [line.split() for line in lines]
answer_1 = 0
answer_2 = 0


def is_safe(
    record: list[int],
) -> bool:
    prev: int = record[0]
    ascending: bool = record[1] > prev

    for level in record[1:]:
        cur: int = level
        if ascending is True:
            if cur < prev or cur - prev > 3 or cur - prev < 1:
                return False
        if ascending is False:
            if prev < cur or prev - cur > 3 or prev - cur < 1:
                return False
        prev = cur
    return True


for line in lines_split:
    record = list(map(int, line))
    if is_safe(record):
        answer_1 += 1
        answer_2 += 1
    else:
        for i in range(0, len(record)):
            if is_safe(record[:i] + record[i + 1 :]):
                answer_2 += 1
                break

print(answer_1)
print(answer_2)
