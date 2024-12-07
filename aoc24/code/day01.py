import numpy as np
import pandas as pd

from aoc24.input import read_input_lines

lines: list[str] = read_input_lines(day=1)
lines_split: list[list[str]] = [line.split() for line in lines]
answer_1: int = 0
answer_2: int = 0

df = pd.DataFrame(data=lines_split, columns=["left", "right"])

left = df["left"].astype(int).sort_values(ignore_index=True)
right = df["right"].astype(int).sort_values(ignore_index=True)
answer_1 = np.abs(left - right).sum()

right_value_counts = right.value_counts()
left_in_right = right_value_counts.index.intersection(left)  # type: ignore
left_in_right_counts = right_value_counts[left_in_right]
answer_2 = (left_in_right_counts * left_in_right).sum()

print(answer_1)
print(answer_2)
