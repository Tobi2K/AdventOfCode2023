import re
import sys
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))


def first_task(path):
    sum_all = 0
    with open(path, "r") as f:
        for line in f.readlines():
            # remove all characters, except digits
            line = re.sub("\D", "", line)
            # get first and last string element
            num_str = line[0] + line[-1]
            # convert and sum number
            sum_all += int(num_str)
    return sum_all


def second_task(path):
    sum_all = 0
    with open(path, "r") as f:
        for line in f.readlines():
            # replace all written digits, iteratively!
            # We keep first and last symbols to combat overlaps, e.g. twone is 21 (where applicable)
            # For example, 'four' has no overlap with any other numbers
            line = (
                line.replace("one", "o1e")
                .replace("two", "t2o")
                .replace("three", "t3e")
                .replace("four", "4")
                .replace("five", "5e")
                .replace("six", "6")
                .replace("seven", "7n")
                .replace("eight", "e8t")
                .replace("nine", "n9e")
            )

            # remove all characters, except digits
            line = re.sub("\D", "", line)
            # get first and last string element
            num_str = line[0] + line[-1]
            # convert and sum number
            sum_all += int(num_str)

    return sum_all


if __name__ == "__main__":
    print(first_task("Day1/input.txt"))
    print(second_task("Day1/input.txt"))
