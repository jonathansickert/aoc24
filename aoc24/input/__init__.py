import os
from pathlib import Path

import requests
from dotenv import load_dotenv

INPUT_BASE: Path = Path(__file__).parent

load_dotenv()


def get_puzzle_input_path(day: int) -> Path:
    return INPUT_BASE / ("day" + str(day).rjust(2, "0"))


def read_puzzle_input(day: int) -> str:
    path: Path = get_puzzle_input_path(day=day)
    if path.exists():
        with open(path, "r") as file:
            input: str = file.read()
        return input

    cookie: str | None = os.environ.get("AOC_SESSION_COOKIE")
    if cookie is not None:
        response: requests.Response = requests.get(
            f"https://adventofcode.com/2024/day/{day}/input",
            cookies={"session": cookie},
        )
        input: str = response.text
        with open(path, "w") as file:
            file.write(input)
        return input
    raise Exception


def read_puzzle_input_lines(day: int) -> list[str]:
    input: str = read_puzzle_input(day=day)
    return [line.replace("\n", "") for line in input.split()]
