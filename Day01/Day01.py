import re


def first_task(inp):
    sum_all = 0

    for line in inp:
        # remove all characters, except digits
        line = re.sub("\D", "", line)
        # get first and last string element
        num_str = line[0] + line[-1]
        # convert and sum number
        sum_all += int(num_str)
    return sum_all


def second_task(inp):
    sum_all = 0
    for line in inp:
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


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
