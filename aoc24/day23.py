from collections import defaultdict

from aoc24.aoc_decorator import solves_puzzle


@solves_puzzle(day=23, part=1)
def solve_part_1(input: str) -> int:
    conns: dict[str, set[str]] = defaultdict(set)

    for line in input.splitlines():
        a, b = line.split("-")
        conns[a].add(b)
        conns[b].add(a)

    sets: set[frozenset[str]] = set()
    for a in conns:
        if a.startswith("t"):
            for b in conns[a]:
                for c in conns[b]:
                    if c in conns[a]:
                        sets.add(frozenset((a, b, c)))

    return len(sets)


@solves_puzzle(day=23, part=2)
def solve_part_2(input: str) -> int:
    conns: dict[str, set[str]] = defaultdict(set)

    for line in input.splitlines():
        a, b = line.split("-")
        conns[a].add(b)
        conns[b].add(a)

    sets: set[frozenset[str]] = set()
    for a in conns:
        for b in conns[a]:
            sets.add(frozenset((a, b)))

        for s in sets.copy():
            if s.issubset(conns[a]):
                sets.remove(s)
                sets.add(frozenset((a, *s)))

    max_length: int = max(len(s) for s in sets)
    sets_with_max_length: list[frozenset[str]] = [
        s for s in sets if len(s) == max_length
    ]
    print(",".join(sorted(list(sets_with_max_length.pop()))))

    return 0


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
