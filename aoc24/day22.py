from collections import Counter

from aoc24.aoc_decorator import solves_puzzle


def get_n_secrets(initial: int, n: int) -> list[int]:
    secret: int = initial
    secrets: list[int] = [initial]
    mask: int = 16777216 - 1

    for _ in range(n):
        secret ^= secret << 6
        secret &= mask
        secret ^= secret >> 5
        secret &= mask
        secret ^= secret << 11
        secret &= mask
        secrets.append(secret)

    return secrets


def get_prices(secrets: list[int]) -> dict:
    counter = Counter()

    for i in range(4, len(secrets) - 1):
        c3: int = secrets[i - 3] % 10 - secrets[i - 4] % 10
        c2: int = secrets[i - 2] % 10 - secrets[i - 3] % 10
        c1: int = secrets[i - 1] % 10 - secrets[i - 2] % 10
        c0: int = secrets[i - 0] % 10 - secrets[i - 1] % 10

        if (c3, c2, c1, c0) in counter:
            continue

        counter[c3, c2, c1, c0] = secrets[i] % 10

    return counter


@solves_puzzle(day=22)
def solve_both_parts(input: str) -> tuple[int, int]:
    secrets: list[int] = list(map(int, input.splitlines()))

    answer1: int = 0
    counter = Counter()

    for secret in secrets:
        secrets = get_n_secrets(secret, 2000)
        answer1 += secrets[-1]
        counter += get_prices(secrets)

    return answer1, max(counter.values())


if __name__ == "__main__":
    solve_both_parts()
