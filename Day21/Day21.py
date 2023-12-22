import numpy as np

def get_maze(inp):
    maze = []
    start = None
    for row, line in enumerate(inp):
        maze.append(list(line ))
        if "S" in line:
            start = (row , line.index("S") )

    return maze, start

def get_padded_maze(inp):
    maze = [list("0" * (len(inp[0]) + 2))]
    start = None
    for row, line in enumerate(inp):
        maze.append(list("0" + line + "0"))
        if "S" in line:
            start = (row + 1, line.index("S") + 1)

    maze.append(list("0" * (len(inp[0]) + 2)))

    return maze, start


def first_task(inp, step_limit=64):
    maze, start = get_padded_maze(inp)
    copy_maze, _ = get_padded_maze(inp)

    return construct_and_reachability_maze(maze, copy_maze, start, step_limit)


# Idea: The area grows quadratically wrt to length/height of input
# Approximate polynomial using the first three points (after 64 steps, 64 + len(inp), 64 + 2 * len(inp))
def second_task(inp, step, goal, poly_points_save=None):
    maze, start = get_maze(inp)
    if not poly_points_save:
        poly_points = []
        for i in range(3):
            poly_points.append(
                construct_and_reachability_maze_with_expansion(
                    maze, start, step + i * len(maze)
                )
            )
    else:
        poly_points = poly_points_save
    return extrapolate_value(poly_points, goal // len(maze))

def construct_and_reachability_maze_with_expansion(maze, start, limit):
    positions = [(start, 0)]

    seen_states = set()
    positions_on_limit = set()
    while positions:
        position, steps = positions.pop(0)
        if (position, steps) in seen_states:
            continue
        if steps == limit:
            positions_on_limit.add(position)
            continue
        seen_states.add((position, steps))
        neighbors = get_neighbors_with_expansion(maze, position)
        for n in neighbors:
            positions.append((n, steps + 1))
    return len(positions_on_limit)

def get_neighbors_with_expansion(maze, position):
    legal_neighbors = []
    x, y = position
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if maze[(x + dx) % len(maze)][(y + dy) % len(maze[0])] != "#":
            legal_neighbors.append((x + dx, y + dy))

    return legal_neighbors

def construct_and_reachability_maze(maze, copy_maze, start, limit):
    positions = [(start, 0)]

    seen_states = set()

    while positions:
        position, steps = positions.pop(0)
        if (position, steps) in seen_states:
            continue
        if steps == limit:
            copy_maze[position[0]][position[1]] = "$"
            continue
        seen_states.add((position, steps))
        neighbors = get_neighbors(maze, position)
        for n in neighbors:
            positions.append((n, steps + 1))
    return count_reachable(copy_maze)


def get_neighbors(maze, position):
    legal_neighbors = []
    x, y = position
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if maze[x + dx][y + dy] in "S.":
            legal_neighbors.append((x + dx, y + dy))

    return legal_neighbors


def count_reachable(maze):
    count = 0
    for row in maze:
        count += row.count("$")
    return count


# Thanks numpy
def extrapolate_value(poly_points, steps):
    coef = np.polyfit([0, 1, 2], poly_points, 2)

    # Evaluate the quadratic equation at the given x value
    result = np.polyval(coef, steps)
    return round(result)


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp, 6))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    # Extrapolation does not work for test input, because start col & row is not empty (does not create a perfectly symmetrical diamond structure)
    print("Second Task, Test Input:\t", second_task(test_inp, 6, 100))
    # 65, because 26501365 % 131 (len of input) = 65
    # Used to approximate 202300 * 131 + 65 = 26501365 using x=0,1,2 and 65 + x * 131 
    print(
        "Second Task, Task Input:\t",
        second_task(
            task_inp,
            65,
            26501365,
            poly_points_save=[3752, 33614, 93252]
        ),
    )
