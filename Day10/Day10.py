import sys
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = "Day10/"

dir_map = {
        'N': {'|': 'N', 'L': 'W', 'J': 'E'},
        'E': {'-': 'E', 'F': 'N', 'L': 'S'},
        'S': {'|': 'S', '7': 'E', 'F': 'W'},
        'W': {'-': 'W', 'J': 'S', '7': 'N'},
    }
x_y_change = {'N': (1, 0), 'E': (0, -1), 'S': (-1, 0), 'W': (0, 1)}

def pad_input(inp):
    chars = [list('0' * (len(inp[0]) + 2))]
    S = None
    for idx, line in enumerate(inp):
        if "S" in line:
            S = (idx + 1, line.index("S") + 1)
        chars.append(list('0' + line + '0'))
    chars.append(list('0' * (len(inp[0]) + 2)))
    
    return chars, S

def find_S_replacement(chars, S):
    coming_from = ""
    possible_chars = []
    # Find out where we are coming from
    # Check above
    if chars[S[0] - 1][S[1]] in ["|", "7", "F"]:
        if coming_from == "":
            coming_from = "S"
        possible_chars.append(set(["|", "L", "J"]))
    # Check below
    if chars[S[0] + 1][S[1]] in ["|", "L", "J"]:
        if coming_from == "":
            coming_from = "N"
        possible_chars.append(set(["|", "7", "F"]))
    # Check right
    if chars[S[0]][S[1] + 1] in ["-", "J", "7"]:
        if coming_from == "":
            coming_from = "W"
        possible_chars.append(set(["-", "F", "L"]))
    # Check left
    if chars[S[0]][S[1] - 1] in ["-", "F", "L"]:
        if coming_from == "":
            coming_from = "E"
        possible_chars.append(set(["-", "J", "7"]))
        
    if len(possible_chars) != 2:
        raise Exception("S must have two connections!")
    
    S_replacement = possible_chars[0].intersection(possible_chars[1]).pop()
    return coming_from, S_replacement

def first_task(path):
    inp = get_file_as_lines(path)
    
    chars, S = pad_input(inp)
    
    next_char_pos = S
    
    coming_from, x = find_S_replacement(chars, S)
    chars[S[0]][S[1]] = x
    path_length = 0
    while next_char_pos != S or path_length == 0:
        path_length += 1
        y_pos, x_pos = next_char_pos
        delta_y, delta_x = x_y_change[coming_from]
        next_char = chars[y_pos + delta_y][x_pos + delta_x]
        next_char_pos = (y_pos + delta_y, x_pos + delta_x)
        coming_from = dir_map[coming_from][next_char]
    
    return int(path_length / 2)

# Simple line integral with Green's theroem https://en.wikipedia.org/wiki/Green%27s_theorem
# Props to my calculas course :)
def second_task(path):
    inp = get_file_as_lines(path)
    
    chars, S = pad_input(inp)
    
    next_char_pos = S
    
    coming_from, x = find_S_replacement(chars, S)
    chars[S[0]][S[1]] = x
    path_length = 0
    area = 0
    while next_char_pos != S or path_length == 0:
        path_length += 1
        y_pos, x_pos = next_char_pos
        delta_y, delta_x = x_y_change[coming_from]
        area += x_pos * delta_y # Line Integral
        next_char = chars[y_pos + delta_y][x_pos + delta_x]
        next_char_pos = (y_pos + delta_y, x_pos + delta_x)
        coming_from = dir_map[coming_from][next_char]

    return area - path_length // 2 + 1



if __name__ == "__main__":
    print("First Task, Test Input:\t\t", first_task(FOLDER + "test-input.txt"))
    print("First Task, Test Input 2:\t", first_task(FOLDER + "test-input2.txt"))
    print("First Task, Task Input:\t\t", first_task(FOLDER + "input.txt"))
    print("Second Task, Test Input 3:\t", second_task(FOLDER + "test-input3.txt"))
    print("Second Task, Task Input:\t", second_task(FOLDER + "input.txt"))
    
    
    
