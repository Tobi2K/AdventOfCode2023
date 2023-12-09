import sys
import re
import math
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = "Day9/"

# Split and convert input into lists of numbers
def get_sequences(inp):
    seqs = []
    for line in inp:
        seqs.append([int(x) for x in re.findall(r"-?\d+", line)])
    return seqs

def first_task(path):
    inp = get_file_as_lines(path)
    next_val = 0
    for seq in get_sequences(inp):
        next_val += interpolate_me(seq)
    # As interpolation may lead to some inaccuracies, round the number
    return round(next_val)

# Second part is just the same as first, except we want to reverse our arrays
def second_task(path):
    inp = get_file_as_lines(path)
    next_val = 0
    for seq in get_sequences(inp):
        next_val += interpolate_me(seq[::-1])
    # As interpolation may lead to some inaccuracies, round the number
    return round(next_val)

# Just use lagrange interpolation, as it is always a defined change
# https://en.wikipedia.org/wiki/Lagrange_polynomial
def interpolate_me(arr):
    # Number of points
    k = len(arr)
    # Our 'highest' point
    x = len(arr)
    # Keep track of our interpolation value sum
    val = 0
    # Go through every point
    for x_j, y_j in enumerate(arr):
        # Compute basis polynomial for x_j
        l_j_x = math.prod((x - x_m) / (x_j - x_m) for x_m in range(k) if x_m != x_j)
        # Add product of basis polynomial and y_j value (our next point) to interpolation sum
        val += y_j * l_j_x
        
    # Return sum of all interpolated values for all points
    return val

if __name__ == "__main__":
    print("First Task, Test Input:\t\t", first_task(FOLDER + "test-input.txt"))
    print("First Task, Task Input:\t\t", first_task(FOLDER + "input.txt"))
    print("Second Task, Test Input:\t", second_task(FOLDER + "test-input.txt"))
    print("Second Task, Task Input:\t", second_task(FOLDER + "input.txt"))