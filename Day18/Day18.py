import sys
from pathlib import Path
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = "Day18/"


def first_task(path):
    inp = get_file_as_lines(path)
    directions = []
    lengths = []
    for line in inp:
        s = line.split(" ")
        directions.append(s[0])
        lengths.append(int(s[1]))
        
    return get_area(lengths, directions)

def second_task(path):
    inp = get_file_as_lines(path)
    colors = []
    for line in inp:
        s = line.split(" ")
        # remove all unnecessary information
        colors.append(s[2].replace("#", "").replace("(", "").replace(")", ""))
    
    directions = []
    lengths = []
    dir_map = {"0": "R", "1": "D", "2": "L", "3": "U"}
    for c in colors:
        # Find direction based on last char
        directions.append(dir_map[c[-1]])
        # Convert all but last char to int
        lengths.append(int(c[:-1], 16))
        
    return get_area(lengths, directions)


# The spanned area is always a polygon, simply track all corner nodes of the polygon
# Calculate area, for example using https://en.wikipedia.org/wiki/Pick's_theorem (transformed to get number of integer points in traced area (i))
# Pick's theorem simply requires tracking the number of nodes on the edge (i.e., the steps we take in each direction)
# The area in the traced area can be calculated using Gauss's area formula
def get_area(lengths, directions):
    trench_edges = 0
    trench_nodes = []        
    cur_point = (0, 0)
    direction_map = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}
    
    for length, direction in zip (lengths, directions):
        x, y = cur_point
        dx, dy = direction_map[direction]
        cur_point = (x + dx * length, y + dy * length)
        trench_edges += length
        trench_nodes.append(cur_point)
        
    # A = i + b/2 - 1
    # <==>
    # i = A - b/2 + 1
    
    # Get A with Gauss's area formula
    element_sums = 0
    for idx in range(len(trench_nodes)):
        xi, yi = trench_nodes[idx]
        xipp, yipp = trench_nodes[(idx + 1) % len(trench_nodes)]
        xi_yipp = xi * yipp
        xipp_yi = xipp * yi
        
        element_sums += xi_yipp - xipp_yi
    A = 0.5 * abs(element_sums)
        
    # return included points + border
    return int(A - trench_edges / 2 + 1) + trench_edges


if __name__ == "__main__":
    print("First Task, Test Input:\t\t", first_task(FOLDER + "test-input.txt"))
    print("First Task, Task Input:\t\t", first_task(FOLDER + "input.txt"))
    print("Second Task, Test Input:\t", second_task(FOLDER + "test-input.txt"))
    print("Second Task, Task Input:\t", second_task(FOLDER + "input.txt"))