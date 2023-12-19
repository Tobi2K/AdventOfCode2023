import math
import re


def first_task(inp):
    instructions = [x for x in inp.pop(0)]
    inp.pop(0)

    maps = dict()

    for line in inp:
        matches = re.search(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line)
        idx, left, right = matches.group(1), matches.group(2), matches.group(3)
        maps[idx] = (left, right)
    current_node = "AAA"
    steps = 0
    while True:
        for inst in instructions:
            steps += 1
            if inst == "L":
                current_node = maps[current_node][0]
            elif inst == "R":
                current_node = maps[current_node][1]

            if current_node == "ZZZ":
                return steps


# Map & check attempt is too slow for second part (steps turn out to be 24035773251517), but:
# As we need to find every path from XXA to XXZ, we can use path length for each such path
# To get from all XXA to a XXZ simultaneosly is then the lcm for all XXA
def second_task(inp):
    instructions = [x for x in inp.pop(0)]
    inp.pop(0)

    maps = dict()
    starts = []

    for line in inp:
        matches = re.search(r"([A-Z1-9]{3}) = \(([A-Z1-9]{3}), ([A-Z1-9]{3})\)", line)
        idx, left, right = matches.group(1), matches.group(2), matches.group(3)
        maps[idx] = (left, right)
        if idx.endswith("A"):
            starts.append(idx)
    cur_lcm = 1
    for cur in starts:
        cur_lcm = math.lcm(cur_lcm, get_path_len(cur, maps, instructions))

    return cur_lcm


def get_path_len(cur_node, maps, instructions):
    steps = 0
    while True:
        for inst in instructions:
            steps += 1
            if inst == "L":
                cur_node = maps[cur_node][0]
            elif inst == "R":
                cur_node = maps[cur_node][1]
            if cur_node.endswith("Z"):
                return steps


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
