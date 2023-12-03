import re
import sys, os
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

def first_task(path):
    sum_all = 0
    with open(path, 'r') as f:
        for line in f.readlines():
            # remove all characters, except digits
            line = re.sub('\D', '', line)
            # get first and last string element
            num_str = line[0] + line[-1]
            # convert and sum number
            sum_all += int(num_str)
    return sum_all

def second_task(path):
    sum_all = 0
    with open(path, 'r') as f:
        for line in f.readlines():
            edit_line = line
            # replace all written digits, iteratively!
            # We keep first and last symbols to combat overlaps, e.g. twone is 21 (where applicable)
            # For example, 'four' has no overlap with any other numbers
            edit_line = edit_line.replace("one", 'o1e')
            edit_line = edit_line.replace("two", 't2o')
            edit_line = edit_line.replace("three", 't3e')
            edit_line = edit_line.replace("four", '4')
            edit_line = edit_line.replace("five", '5e')
            edit_line = edit_line.replace("six", '6')
            edit_line = edit_line.replace("seven", '7n')
            edit_line = edit_line.replace("eight", 'e8t')
            edit_line = edit_line.replace("nine", 'n9e')
            # Old solution, before I knew, that eighthree would be 83 and not 8hree
            # i = 0
            # while i < len(line) - 3:
            #     #print(i)
            #     inc = 3
            #     while i+inc <= len(line):
            #         if inc > 6:
            #             break
            #         cur_sub_str = line[i:i+inc]
            #         #print(cur_sub_str)
            #         if cur_sub_str == "one":
            #             edit_line = edit_line.replace("one", 'o1e', 1)
            #             i += 2
            #             break
            #         if cur_sub_str == "two":
            #             edit_line = edit_line.replace("two", 't2o', 1)
            #             i += 2
            #             break
            #         if cur_sub_str == "three":
            #             edit_line = edit_line.replace("three", 't3e', 1)
            #             i += 4
            #             break
            #         if cur_sub_str == "four":
            #             edit_line = edit_line.replace("four", 'f4r', 1)
            #             i += 3
            #             break
            #         if cur_sub_str == "five":
            #             edit_line = edit_line.replace("five", 'f5e', 1)
            #             i += 3
            #             break
            #         if cur_sub_str == "six":
            #             edit_line = edit_line.replace("six", 's6x', 1)
            #             i += 2
            #             break
            #         if cur_sub_str == "seven":
            #             edit_line = edit_line.replace("seven", 's7n', 1)
            #             i += 4
            #             break
            #         if cur_sub_str == "eight":
            #             edit_line = edit_line.replace("eight", 'e8t', 1)
            #             i += 4
            #             break
            #         if cur_sub_str == "nine":
            #             edit_line = edit_line.replace("nine", 'n9e', 1)
            #             i += 3
            #             break
            #         inc += 1
            #     i += 1
            save = edit_line
            # remove all characters, except digits
            line = re.sub('\D', '', edit_line)
            # get first and last string element
            num_str = line[0] + line[-1]
            # convert and sum number
            sum_all += int(num_str)
            
    return sum_all

if __name__=="__main__":
    print(first_task("Day1/input.txt"))
    print(second_task("Day1/input.txt"))
            