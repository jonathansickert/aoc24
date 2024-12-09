from aoc24.input import read_input

input: str = read_input(day=9)
vals: list[int] = list(map(int, input.replace("\n", "")))
answer_1: int = 0
answer_2: int = 0


ids1 = iter(range(len(vals)))
files1 = [
    val for i, x in enumerate(vals) for val in [next(ids1) if i % 2 == 0 else None] * x
]
j: int = len(files1) - 1

for i in range(len(files1)):
    while not files1[j]:
        j -= 1
    if j <= i:
        break
    if files1[i] is None:
        files1[i], files1[j] = files1[j], files1[i]
    answer_1 += i * files1[i]  # type: ignore


def search(size: int) -> int:
    for i, (length, id, _) in enumerate(files2):
        if id is None and length >= size:
            return i
    return -1


ids2 = iter(range(len(vals)))
files2 = [(x, next(ids2) if i % 2 == 0 else None, 0) for i, x in enumerate(vals)]
acc = []

while len(files2) > 0:
    length, id, visited = files2.pop()
    if visited == 1 or id is None or (i := search(length)) == -1:
        acc += [id] * length
        continue
    free_lenght, _, _ = files2[i]
    files2[i] = (length, id, 1)
    if (new_free_length := free_lenght - length) > 0:
        files2.insert(i + 1, (new_free_length, None, 0))
    files2.append((length, None, 0))

answer_2 = sum([i * val for i, val in enumerate(acc[::-1]) if val is not None])

print(answer_1)
print(answer_2)
