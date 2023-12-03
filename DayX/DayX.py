import sys
from pathlib import Path

from AdventOfCode2023.utils import get_file_as_lines

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

FOLDER = "DayX/"

def first_task(path):
    inp = get_file_as_lines(path)
    
    return

def second_task(path):
    inp = get_file_as_lines(path)
    
    return


if __name__ == "__main__":
    print(first_task(FOLDER + "test-input.txt"))
    print(first_task(FOLDER + "input.txt"))
    print(second_task(FOLDER + "test-input.txt"))
    print(second_task(FOLDER + "input.txt"))