from collections import Counter


# Map letters and numbers, so we can simply use sorted()
def map_letters(string):
    return (
        string.replace("K", "B")
        .replace("Q", "C")
        .replace("J", "D")
        .replace("T", "E")
        .replace("9", "F")
        .replace("8", "G")
        .replace("7", "H")
        .replace("6", "I")
        .replace("5", "J")
        .replace("4", "K")
        .replace("3", "L")
        .replace("2", "M")
    )


def first_task(inp):
    inp = [(map_letters(x.split(" ")[0]), int(x.split(" ")[1])) for x in inp]

    high_card = []
    pair = []
    two_pair = []
    three_of_a_kind = []
    full_house = []
    four_of_a_kind = []
    five_of_a_kind = []

    for t in inp:
        hand, bid = t
        count = Counter(hand)
        # Get number of unique cards
        unique_len = len(sorted(count))
        # Get the amount of the highest card
        _, highest_count = count.most_common(1)[0]

        # Must be high card
        if unique_len == 5:
            high_card.append(t)
        # Must be pair
        elif unique_len == 4:
            pair.append(t)
        # Must be three of a kind or two pair
        elif unique_len == 3:
            # Is three of a kind
            if highest_count == 3:
                three_of_a_kind.append(t)
            # Is two pair
            else:
                two_pair.append(t)
        # Must be four of a kind or full house
        elif unique_len == 2:
            # Is four of a kind
            if highest_count == 4:
                four_of_a_kind.append(t)
            # Is full house
            else:
                full_house.append(t)
        # Must be five of a kind
        elif unique_len == 1:
            five_of_a_kind.append(t)

    # Go through sorted hands and calculate total winnings
    rank = 1
    total_winnings = 0
    for arr in [
        high_card,
        pair,
        two_pair,
        three_of_a_kind,
        full_house,
        four_of_a_kind,
        five_of_a_kind,
    ]:
        for _, bid in sorted(arr, key=lambda x: x[0], reverse=True):
            total_winnings += rank * bid
            rank += 1

    return total_winnings


# Map letters and numbers, so we can simply use sorted(), but now map J to lowest value (here N)
def second_map_letters(string):
    return (
        string.replace("K", "B")
        .replace("Q", "C")
        .replace("J", "N")
        .replace("T", "E")
        .replace("9", "F")
        .replace("8", "G")
        .replace("7", "H")
        .replace("6", "I")
        .replace("5", "J")
        .replace("4", "K")
        .replace("3", "L")
        .replace("2", "M")
    )


def second_task(inp):
    inp = [(second_map_letters(x.split(" ")[0]), int(x.split(" ")[1])) for x in inp]

    high_card = []
    pair = []
    two_pair = []
    three_of_a_kind = []
    full_house = []
    four_of_a_kind = []
    five_of_a_kind = []

    for t in inp:
        hand, bid = t
        # Get count of each letter
        count = Counter(hand)
        j_count = count["N"]
        # If our hand is only jokers, return
        if j_count == 5:
            five_of_a_kind.append(t)
            continue
        # Remove jokers from hand
        del count["N"]
        _, highest_count = count.most_common(1)[0]
        # Get new number of unique letters (without jokers)
        unique_len_after_j = len(sorted(count))

        # Get highest count including jokers
        count_with_joker = highest_count + j_count

        # Flip the way of checking
        # Must be five of a kind
        if count_with_joker == 5:
            five_of_a_kind.append(t)
        # Must be four of a kind
        elif count_with_joker == 4:
            four_of_a_kind.append(t)
        # Must be three of a kind or full house
        elif count_with_joker == 3:
            # three of a kind, other two cards are different
            if unique_len_after_j == 3:
                three_of_a_kind.append(t)
            else:
                full_house.append(t)
        # Must be pair or two pair
        elif count_with_joker == 2:
            # pair, other three cards are different
            if unique_len_after_j == 4:
                pair.append(t)
            else:
                two_pair.append(t)
        elif count_with_joker == 1:
            high_card.append(t)

    # Go through sorted hands and calculate total winnings
    rank = 1
    total_winnings = 0
    for arr in [
        high_card,
        pair,
        two_pair,
        three_of_a_kind,
        full_house,
        four_of_a_kind,
        five_of_a_kind,
    ]:
        for _, bid in sorted(arr, key=lambda x: x[0], reverse=True):
            total_winnings += rank * bid
            rank += 1

    return total_winnings


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
