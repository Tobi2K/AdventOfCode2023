import math
import re


# Split and convert input into lists of numbers
def get_sequences(inp):
    seqs = []
    for line in inp:
        seqs.append([int(x) for x in re.findall(r"-?\d+", line)])
    return seqs


def first_task(inp):
    next_val = 0
    for seq in get_sequences(inp):
        next_val += interpolate_me(seq)
    # As interpolation may lead to some inaccuracies, round the number
    return round(next_val)


# Second part is just the same as first, except we want to reverse our arrays
def second_task(inp):
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


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
