import re


def first_task(inp):
    RED = 12
    GREEN = 13
    BLUE = 14
    id_sum = 0
    for line in inp:
        split = line.replace("\n", "").split(":")
        game_id = re.search(r"Game (\d+)", split[0]).group(1)
        games = split[1].split(";")
        legal = True
        for game in games:
            greens = re.search(r"(\d+) green", game)
            blues = re.search(r"(\d+) blue", game)
            reds = re.search(r"(\d+) red", game)

            for bound, color in zip([GREEN, BLUE, RED], [greens, blues, reds]):
                if color is not None:
                    if int(color.group(1)) > bound:
                        legal = False
                        break
            if not legal:
                break
        if legal:
            id_sum += int(game_id)
    return id_sum


def second_task(inp):
    power_sum = 0
    for line in inp:
        split = line.replace("\n", "").split(":")
        games = split[1].split(";")
        min_green = 0
        min_blue = 0
        min_red = 0
        for game in games:
            greens = re.search(r"(\d+) green", game)
            blues = re.search(r"(\d+) blue", game)
            reds = re.search(r"(\d+) red", game)

            if greens is not None:
                if int(greens.group(1)) > min_green:
                    min_green = int(greens.group(1))
            if blues is not None:
                if int(blues.group(1)) > min_blue:
                    min_blue = int(blues.group(1))
            if reds is not None:
                if int(reds.group(1)) > min_red:
                    min_red = int(reds.group(1))

        power_sum += min_green * min_blue * min_red
    return power_sum


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
