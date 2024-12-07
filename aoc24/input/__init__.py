from pathlib import Path

INPUT_BASE: Path = Path(__file__).parent


def get_input_path(day: int) -> Path:
    path: Path = INPUT_BASE / ("day" + str(day).rjust(2, "0"))

    assert path.exists()

    return path


def read_input(day: int) -> str:
    path: Path = get_input_path(day=day)
    with open(path, "r") as file:
        input: str = file.read()

    return input


def read_input_lines(day: int) -> list[str]:
    path: Path = get_input_path(day=day)
    with open(path, "r") as file:
        lines: list[str] = file.readlines()

    return [line.replace("\n", "") for line in lines]
