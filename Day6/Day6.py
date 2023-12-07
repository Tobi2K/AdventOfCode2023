import sys
import re
import math
from pathlib import Path
from sympy import symbols, reduce_inequalities

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = "Day6/"

# Formulate the distance as a formula and solve for the boundaries
def solve_equation(time, dist):
    hold_time = symbols('h')
    # Equation is: <Holding Time> * (<Race Time> - <Holding Time>)
    # <Holding Time> is directly equivalent to the speed of the boat and <Race Time> reduces linearly with <Holding Time>
    # Find boundaries, where equation would exactly yield the distance recorde (`dist`)
    eq = reduce_inequalities([dist <= hold_time * (time - hold_time), hold_time * (time - hold_time) <= dist], hold_time)
    
    # Extract (and sort) boundaries of our inequality
    constants = sorted([arg.rhs.evalf() if arg.lhs == hold_time else arg.lhs.evalf() for arg in eq.args])

    # Get number of possible holding times between boundaries
    return (math.ceil(constants[1] - 1) - math.floor(constants[0] + 1)) + 1

def first_task(path):
    inp = get_file_as_lines(path)
    # Extract times and distances as a list
    times = [int(x) for x in re.findall(r"\d+", inp[0])]
    dists = [int(x) for x in re.findall(r"\d+", inp[1])]
    
    # Keep track of our product
    run_prod = 1
    for time, dist in zip(times, dists):
        run_prod *= solve_equation(time, dist)
    
    return run_prod


def second_task(path):
    inp = get_file_as_lines(path)
    # Remove spaces and extract number
    time = int(re.findall(r"\d+", inp[0].replace(" ", ""))[0])
    dist = int(re.findall(r"\d+", inp[1].replace(" ", ""))[0])
    # Solve equation for combined time and distance
    return solve_equation(time, dist)
    


if __name__ == "__main__":
    print("First Task, Test Input:\t\t", first_task(FOLDER + "test-input.txt"))
    print("First Task, Task Input:\t\t", first_task(FOLDER + "input.txt"))
    print("Second Task, Test Input:\t", second_task(FOLDER + "test-input.txt"))
    print("Second Task, Task Input:\t", second_task(FOLDER + "input.txt"))