import argparse
import importlib


def get_file_as_lines(path):
    with open(path, "r") as f:
        tmp_lines = f.readlines()
        lines = []
        for line in tmp_lines:
            lines.append(line.replace("\n", ""))
        return lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AoC Days.")
    parser.add_argument("day", metavar="D", type=int, help="Day number to run")
    args = parser.parse_args()
    day_num = f"{args.day:02}"
    module = importlib.import_module("Day" + day_num + "." + "Day" + day_num)
    test_inp = get_file_as_lines("Day" + day_num + "/test-input.txt")
    task_inp = get_file_as_lines("Day" + day_num + "/input.txt")
    module.main(test_inp, task_inp)
