import copy


# Function to add one row and col of '0's to the edge of an array
def pad_and_split_contraption(inp):
    maze = [["0"] * (len(inp[0]) + 2)]
    for line in inp:
        maze.append(list("0" + line.replace("\\", "$") + "0"))

    maze.append(["0"] * (len(inp[0]) + 2))

    return maze


def first_task(inp):
    maze = pad_and_split_contraption(inp)

    light_maze = create_energy_map(maze)

    light_count = count_energy(light_maze)

    return light_count


# Same as task 1, but we do the computation for all possible edge points
def second_task(inp):
    maze = pad_and_split_contraption(inp)
    top_row = [((1, x), "D") for x in range(1, len(maze[0]) - 1)]
    # -2, because of added padding
    bottom_row = [((len(maze) - 2, x), "U") for x in range(1, len(maze[0]) - 1)]
    left_col = [((x, 1), "R") for x in range(1, len(maze) - 1)]
    right_col = [((x, len(maze[0]) - 2), "L") for x in range(1, len(maze) - 1)]
    light_count_best = 0
    for starts in [top_row, bottom_row, left_col, right_col]:
        for pos in starts:
            light_maze = create_energy_map(maze, pos)
            light_count = count_energy(light_maze)
            if light_count > light_count_best:
                light_count_best = light_count

    return light_count_best


# Sum up the number of #s in the given array
def count_energy(light_maze):
    light_count = 0
    for row in light_maze:
        light_count += row.count("#")

    return light_count


def create_energy_map(maze, start_config=((1, 1), "R")):
    maze_copy = copy.deepcopy(maze)
    # Keep track of positions we've seen
    been_there = []
    # Keep track of positions we need to traverse
    positions = [start_config]
    # Move pattern, how position changes
    move = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}
    # Map of next direction, based on the symbol
    move_dict = {
        "U": {".": "U", "/": "R", "$": "L"},
        "L": {".": "L", "/": "D", "$": "U"},
        "D": {".": "D", "/": "L", "$": "R"},
        "R": {".": "R", "/": "U", "$": "D"},
    }

    # While we have open positions
    while len(positions) > 0:
        # Get our current direction and position
        pos_tup = positions.pop(0)
        # Skip positions that we've seen with our current direction
        if pos_tup in been_there:
            continue
        been_there.append(pos_tup)
        cur_pos, direction = pos_tup
        row, col = cur_pos
        cur_char = maze[row][col]
        # Reached border ==> Skip it
        if cur_char == "0":
            continue
        # Light travels through our current pos, so make record of that in maze copy
        maze_copy[row][col] = "#"
        # Split behaviour
        if cur_char == "-":
            # Do not split beam if we're moving with the pipe direction
            if direction in ["L", "R"]:
                cur_char = "."
            # Else create two beams, one left one right
            else:
                positions.append(
                    (tuple([sum(x) for x in zip(cur_pos, move["L"])]), "L")
                )
                positions.append(
                    (tuple([sum(x) for x in zip(cur_pos, move["R"])]), "R")
                )
                continue
        elif cur_char == "|":
            # Do not split beam if we're moving with the pipe direction
            if direction in ["U", "D"]:
                cur_char = "."
            else:
                # Else create two beams, one up one down
                positions.append(
                    (tuple([sum(x) for x in zip(cur_pos, move["U"])]), "U")
                )
                positions.append(
                    (tuple([sum(x) for x in zip(cur_pos, move["D"])]), "D")
                )
                continue
        # If we do not need to split, simply continue on our path according to the current symbol and direction
        new_direction = move_dict[direction][cur_char]
        new_pos = tuple([sum(x) for x in zip(cur_pos, move[new_direction])])
        positions.append((new_pos, new_direction))

    return maze_copy


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
