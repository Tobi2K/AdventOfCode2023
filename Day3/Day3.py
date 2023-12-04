import sys
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

def extend_and_get_array(inp):
    char_array = []
    # Split all chars into a 2D array, but add a line at the top, bottom, left and right so we don't have to check boundary conditions
    char_array.append(["." for _ in inp[0]])
    for line in inp:
        tmp = ["."]
        tmp.extend([x for x in line])
        tmp.append(".")
        char_array.append(tmp)
    char_array.append(["." for _ in inp[0]])
    return char_array


def first_task(path):
    inp = get_file_as_lines(path)

    char_array = extend_and_get_array(inp)

    part_sum = 0
    for i, line in enumerate(char_array):
        num_string = ""
        is_part = False
        for j, char in enumerate(line):
            if char.isnumeric():
                num_string += char
                if not is_part:
                    is_part = check_for_symbol(char_array, i, j)
            else:
                if num_string != "" and is_part:
                    print("Got number", num_string)
                    part_sum += int(num_string)
                    num_string = ""
                    is_part = False
                else:
                    num_string = ""
                    is_part = False

    return part_sum


def check_for_symbol(char_array, row, col):
    check_against = [".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # Row above
    if char_array[row - 1][col - 1] not in check_against:
        return True
    if char_array[row - 1][col] not in check_against:
        return True
    if char_array[row - 1][col + 1] not in check_against:
        return True

    # Row below
    if char_array[row + 1][col - 1] not in check_against:
        return True
    if char_array[row + 1][col] not in check_against:
        return True
    if char_array[row + 1][col + 1] not in check_against:
        return True

    # Left and right, same row
    if char_array[row][col - 1] not in check_against:
        return True
    if char_array[row][col + 1] not in check_against:
        return True

    return False


def second_task(path):
    inp = get_file_as_lines(path)

    char_array = extend_and_get_array(inp)
    gear_ratio_sum = 0
    for i, line in enumerate(char_array):
        for j, char in enumerate(line):
            if char == "*":
                gear_ratio_sum += check_for_ratio(char_array, i, j)

    return gear_ratio_sum


def check_for_ratio(char_array, row, col):
    # Keep track of gear parts
    gear_ratio = []

    # Keep track of where numbers are
    top_left = False
    top_middle = False
    top_right = False
    bottom_left = False
    bottom_middle = False
    bottom_right = False
    # Row above
    if char_array[row - 1][col - 1].isnumeric():
        top_left = True
    if char_array[row - 1][col].isnumeric():
        top_middle = True
    if char_array[row - 1][col + 1].isnumeric():
        top_right = True

    # Row below
    if char_array[row + 1][col - 1].isnumeric():
        bottom_left = True
    if char_array[row + 1][col].isnumeric():
        bottom_middle = True
    if char_array[row + 1][col + 1].isnumeric():
        bottom_right = True

    # Do not count any found numbers twice
    if top_left and top_middle and top_right:
        gear_ratio.append(extract_number(char_array[row - 1], col - 1))
    elif top_middle:
        if top_left:
            gear_ratio.append(extract_number(char_array[row - 1], col - 1))
        elif top_right:
            gear_ratio.append(extract_number(char_array[row - 1], col))
        else:
            gear_ratio.append(int(char_array[row - 1][col]))
    else:
        if top_left:
            gear_ratio.append(extract_number(char_array[row - 1], col - 1))
        if top_right:
            gear_ratio.append(extract_number(char_array[row - 1], col + 1))

    # Do not count any found numbers twice
    if bottom_left and bottom_middle and bottom_right:
        gear_ratio.append(extract_number(char_array[row + 1], col - 1))
    elif bottom_middle:
        if bottom_left:
            gear_ratio.append(extract_number(char_array[row + 1], col - 1))
        elif bottom_right:
            gear_ratio.append(extract_number(char_array[row + 1], col))
        else:
            gear_ratio.append(int(char_array[row + 1][col]))
    else:
        if bottom_left:
            gear_ratio.append(extract_number(char_array[row + 1], col - 1))
        if bottom_right:
            gear_ratio.append(extract_number(char_array[row + 1], col + 1))

    # Left and right, same row
    if char_array[row][col - 1].isnumeric():
        gear_ratio.append(extract_number(char_array[row], col - 1))
    if char_array[row][col + 1].isnumeric():
        gear_ratio.append(extract_number(char_array[row], col + 1))

    if len(gear_ratio) == 2:
        return gear_ratio[0] * gear_ratio[1]
    else:
        return 0


def extract_number(row, col):
    left_index = col
    while row[left_index - 1].isnumeric():
        left_index -= 1

    num_string = ""
    while row[left_index].isnumeric():
        num_string += row[left_index]
        left_index += 1
    return int(num_string)


if __name__ == "__main__":
    print(first_task("Day3/test-input.txt"))
    print(first_task("Day3/input.txt"))
    print(second_task("Day3/test-input.txt"))
    print(second_task("Day3/input.txt"))
