import sys
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = TODO "DayX/"

def first_task(path):
    inp = get_file_as_lines(path)
    
    return

def second_task(path):
    inp = get_file_as_lines(path)
    
    return


if __name__ == "__main__":
    print("First Task, Test Input:\t\t", first_task(FOLDER + "test-input.txt"))
    print("First Task, Task Input:\t\t", first_task(FOLDER + "input.txt"))
    print("Second Task, Test Input:\t", second_task(FOLDER + "test-input.txt"))
    print("Second Task, Task Input:\t", second_task(FOLDER + "input.txt"))