import sys
import numpy as np
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = "Day11/"


def expand_universe(path, expansion_factor=1000000):
    inp = get_file_as_lines(path)
    universe = []
    # Keep track of rows and cols (indices) that have to be expanded 
    expand_rows = []
    expand_cols = []
    # Find empty rows
    for idx, line in enumerate(inp):
        universe.append(list(line))
        if len(line.replace(".", "")) == 0:
            expand_rows.append(idx)
    
    # Transpose to easily navigate columns and find empty cols
    universe = list(map(list, np.transpose(universe)))
    new_universe = []
    for idx, line in enumerate(universe):
        new_universe.append(list(line))
        if "#" not in line:
            expand_cols.append(idx)
    # Transpose back
    universe = list(map(list, np.transpose(new_universe)))
    # Get points of galaxies
    points = []
    for idx, line in enumerate(universe):
        for idy, char in enumerate(line):
            if char == "#":
                points.append((idx, idy))
    # Keep track of distance sum
    distance_sum = 0
    # Go through all points and calc distance
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        for j in range(i + 1, len(points)):
            x2, y2 = points[j]
            # Create sets of column and row indices that are between points
            row_set = set(range(min(x1, x2), max(x1, x2)))
            col_set = set(range(min(y1, y2), max(y1, y2)))
            # Get number of rows and cols that have to be expanded
            row_expansion = row_set.intersection(expand_rows)
            col_expansion = col_set.intersection(expand_cols)
            expansion_count = len(row_expansion) + len(col_expansion)
            # Calc manhattan distance and add expansion factor (-1, because implicitly each row is added once)
            distance_sum += abs(x1 - x2) + abs(y1 - y2) + expansion_count * (expansion_factor - 1)
            
    return distance_sum


if __name__ == "__main__":
    print("First Task, Test Input:\t\t", expand_universe(FOLDER + "test-input.txt", expansion_factor=2))
    print("First Task, Task Input:\t\t", expand_universe(FOLDER + "input.txt", expansion_factor=2))
    print("Second Task, Test Input:\t", expand_universe(FOLDER + "test-input.txt", expansion_factor=1000000))
    print("Second Task, Task Input:\t", expand_universe(FOLDER + "input.txt", expansion_factor=1000000))