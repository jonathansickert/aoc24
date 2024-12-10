from aoc24.aoc_decorator import solves_puzzle


@solves_puzzle(day=9, part=1)
def solve_part_1(input: str) -> int:
    vals: list[int] = list(map(int, input.replace("\n", "")))
    answer1: int = 0
    ids = iter(range(len(vals)))
    files = [
        val
        for i, x in enumerate(vals)
        for val in [next(ids) if i % 2 == 0 else None] * x
    ]
    j: int = len(files) - 1
    for i in range(len(files)):
        while not files[j]:
            j -= 1
        if j <= i:
            break
        if files[i] is None:
            files[i], files[j] = files[j], files[i]
        answer1 += i * files[i]  # type: ignore
    return answer1


def search(size: int, files) -> int:
    for i, (length, id, _) in enumerate(files):
        if id is None and length >= size:
            return i
    return -1


@solves_puzzle(day=9, part=2)
def solve_part_2(input: str) -> int:
    vals: list[int] = list(map(int, input.replace("\n", "")))
    ids = iter(range(len(vals)))
    files = [(x, next(ids) if i % 2 == 0 else None, 0) for i, x in enumerate(vals)]
    acc = []
    while len(files) > 0:
        length, id, visited = files.pop()
        if visited == 1 or id is None or (i := search(length, files)) == -1:
            acc += [id] * length
            continue
        free_lenght, _, _ = files[i]
        files[i] = (length, id, 1)
        if (new_free_length := free_lenght - length) > 0:
            files.insert(i + 1, (new_free_length, None, 0))
        files.append((length, None, 0))
    return sum([i * val for i, val in enumerate(acc[::-1]) if val is not None])


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
