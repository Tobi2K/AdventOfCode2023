import sys
from pathlib import Path
import numpy as np

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = "Day14/"

def first_task(path):
    inp = get_file_as_lines(path)
    tmp = np.array([list(row) for row in inp])
    # North is now index 0
    rotated_rows = np.rot90(tmp)
    
    return calc_load(slide_rocks(rotated_rows))

def second_task(path, cycles=1000000000):
    inp = get_file_as_lines(path)
    
    rows = np.array([list(row) for row in inp])
    rows_dict = dict()
    # Rotate our grid twice, such that it is oriented correctly for later rotation
    # Now South is on top
    rows = np.rot90(rows, k=2)
    row_length = len(rows[0])
    # Cycle through
    for i in range(cycles):
        # Hashable representation of our rows
        rows_as_string = "".join(["".join(row) for row in rows])
        if rows_as_string in rows_dict:
            # Found loop
            # Index of where the loop starts
            loop_start = rows_dict[rows_as_string]
            # The length of our loop
            loop_length = i - loop_start
            # The number of steps (cycles) we have to do after (to complete the cycle count)
            steps_after_loop = (cycles - loop_start) % loop_length
            
            # Get final row by getting the rows at the index loop start + steps after loop:
            final_rows_string = list(rows_dict.keys())[list(rows_dict.values()).index(loop_start + steps_after_loop)]
            
            rows = string_to_rows(final_rows_string, row_length)
            
            break
            
        rows_dict[rows_as_string] = i
        
        rows = cycle_rows(rows)

    # Rotate, so North points left
    rows = np.rot90(rows, axes=(1, 0))    
    return calc_load(rows)

def cycle_rows(rows):
    # rotate and slide rocks 4 times ==> one cycle
    for _ in range(4):
        rot_rows = np.rot90(rows, axes=(1, 0))
        rows = slide_rocks(rot_rows)
    return rows

def string_to_rows(rows_string, row_length):
    return np.array([list(x) for x in np.split(np.array(list(rows_string)), len(rows_string) // row_length)])

def calc_load(rows):
    load_weight = 0
    for row in rows:
        dist = len(row)
        for idx, char in enumerate(row):
            if char == "O":
                load_weight += dist - idx
    return load_weight
    

def slide_rocks(rows):
    for row_idx, row in enumerate(rows):
        add_index = 0
        for idx, char in enumerate(row):
            if char == ".":
                continue
            elif char == "#":
                add_index = idx + 1
            elif char == "O":
                rows[row_idx][idx] = "."
                rows[row_idx][add_index] = "O"
                add_index += 1
                
    return rows
    


if __name__ == "__main__":
    print("First Task, Test Input:\t\t", first_task(FOLDER + "test-input.txt"))
    print("First Task, Task Input:\t\t", first_task(FOLDER + "input.txt"))
    print("Second Task, Test Input:\t", second_task(FOLDER + "test-input.txt"))
    print("Second Task, Task Input:\t", second_task(FOLDER + "input.txt"))