import re


def first_task(inp):
    points = 0
    for line in inp:
        cards = line.split(":")[1].split("|")

        winning_nums = set([int(s) for s in re.findall(r"\d+", cards[0])])
        your_nums = set([int(s) for s in re.findall(r"\d+", cards[1])])

        commons = len(winning_nums.intersection(your_nums))
        if commons > 0:
            points += 2 ** (commons - 1)

    return points


def second_task(inp):
    created_cards = [[0] * len(inp) for _ in inp]
    instances = [1] * len(inp)

    # Set all ids of created cards per card
    for current_card in inp:
        split1 = current_card.split(":")

        card_num = int(re.search(r"Card\s+(\d+)", split1[0]).group(1))

        cards = split1[1].split("|")
        winning_nums = set([int(s) for s in re.findall(r"\d+", cards[0])])
        your_nums = set([int(s) for s in re.findall(r"\d+", cards[1])])

        commons = len(winning_nums.intersection(your_nums))
        for i in range(commons):
            created_cards[card_num - 1][card_num + i] += 1

    # Go through in reverse and sum up cards that will be recursively created
    for arr_idx in range(len(created_cards) - 1, -1, -1):
        cur_card = created_cards[arr_idx]
        card_creation = 0
        for idx, count in enumerate(cur_card):
            card_creation += count * instances[idx]
        instances[arr_idx] += card_creation

    # Sum all cards, because we start with one of each
    return sum(instances)


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
