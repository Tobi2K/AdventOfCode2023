import sys
# Python implementation of a priority queue
import heapq
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = "Day17/"

def first_task(path):
    inp = get_file_as_lines(path)
    
    city_map = [[int(x) for x in line] for line in inp]
    
    min_steps = 0
    max_forward_steps = 3
    
    return find_path(city_map, min_steps, max_forward_steps)

def second_task(path):
    inp = get_file_as_lines(path)
    
    city_map = [[int(x) for x in line] for line in inp]
    
    min_steps = 4
    max_forward_steps = 10
    
    return find_path(city_map, min_steps, max_forward_steps)


def find_path(city_map, min_steps, max_forward_steps):
    # Queue saving the current heat, steps, position and direction
    prio_queue = [(0, 0, (0, 0), (1, 0)), (0, 0, (0, 0), (0, 1))]
    # Keep track of states we've seen
    seen_states = set()
    
    # Goal position (bottom right)
    end_state = (len(city_map) - 1, len(city_map[0]) - 1)
    
    while len(prio_queue) > 0:
        # Get current square
        heat, steps, cur_pos, cur_dir = heapq.heappop(prio_queue)
        # Skip if we've seen it
        if (steps, cur_pos, cur_dir) in seen_states:
            continue
        seen_states.add((steps, cur_pos, cur_dir))
        # If we found the end, return the current heat
        if cur_pos == end_state:
            return heat
        x, y = cur_pos
        dx, dy = cur_dir
        
        # Go one step forward (if it's in bounds and legal)
        if steps < max_forward_steps and 0 <= x + dx < len(city_map) and 0 <= y + dy < len(city_map[0]):
            # calculate new heat and add, if we have not seen it
            new_heat = heat + city_map[x + dx][y + dy]
            new_state = (new_heat, steps + 1, (x + dx, y + dy), (dx, dy))
            if (steps + 1, (x + dx, y + dy), (dx, dy)) not in seen_states:
                heapq.heappush(prio_queue, new_state)
        
        # Go one step right and left (if still in range)
        for dx, dy in [(-dy,dx), (dy,-dx)]:
            # Go one step left/right if it's in bounds and legal
            if steps >= min_steps and 0 <= x + dx < len(city_map) and 0 <= y + dy < len(city_map[0]):
                tmp_x, tmp_y = x + dx, y + dy
                new_heat = heat + city_map[tmp_x][tmp_y]
                heapq.heappush(prio_queue, (new_heat, 1, (tmp_x, tmp_y), (dx, dy)))


    raise Exception("Did not find end path, smth is wrong")


if __name__ == "__main__":
    print("First Task, Test Input:\t\t", first_task(FOLDER + "test-input.txt"))
    print("First Task, Task Input:\t\t", first_task(FOLDER + "input.txt"))
    print("Second Task, Test Input:\t", second_task(FOLDER + "test-input.txt"))
    print("Second Task, Task Input:\t", second_task(FOLDER + "input.txt"))