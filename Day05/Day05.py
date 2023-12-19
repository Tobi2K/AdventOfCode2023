import re


def first_task(inp):
    map_dict = dict()
    cur_transform = [int(s) for s in re.findall(r"\d+", inp.pop(0))]
    inp.pop(0)
    cur_map_word = ""
    cur_map_strings = []
    for line in inp:
        if "map" in line:
            cur_map_word = line.split(" map:")[0]
        elif line == "":
            map_dict[cur_map_word] = cur_map_strings
            cur_map_strings = []
        else:
            # Get range values with regex
            matches = re.search(r"(\d+)\s(\d+)\s(\d+)", line)
            dest_start, source_start, range_len = (
                int(matches.group(1)),
                int(matches.group(2)),
                int(matches.group(3)),
            )
            cur_map_strings.append((dest_start, source_start, range_len))
    map_dict[cur_map_word] = cur_map_strings
    map_order = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    for m in map_order:
        new_transform = []
        for i in cur_transform:
            new_transform.append(change_me(map_dict[m], i))

        cur_transform = new_transform

    return min(cur_transform)


# Gets a mapping from source value to correct new index in target
def change_me(map_strings, source_value):
    for dest_start, source_start, range_len in map_strings:
        if source_start <= source_value < source_start + range_len - 1:
            return dest_start + (source_value - source_start)

    return source_value


def second_task(inp):
    map_dict = dict()
    seeds = [int(s) for s in re.findall(r"\d+", inp.pop(0))]
    inp.pop(0)
    pairs = list(zip(seeds[::2], seeds[1::2]))

    cur_map_word = ""
    cur_map_strings = []
    for line in inp:
        # New map, save it for dictionary
        if "map" in line:
            cur_map_word = line.split(" map:")[0]
        # Ranges are over, save map strings
        elif line == "":
            map_dict[cur_map_word] = cur_map_strings
            cur_map_strings = []
        # Else add new range values
        else:
            # Get range values with regex
            matches = re.search(r"(\d+)\s(\d+)\s(\d+)", line)
            dest_start, source_start, range_len = (
                int(matches.group(1)),
                int(matches.group(2)),
                int(matches.group(3)),
            )
            cur_map_strings.append((dest_start, source_start, range_len))
    map_dict[cur_map_word] = cur_map_strings

    # Reverse map order for proper inversing
    map_order = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]
    map_order.reverse()

    # Bottom up appraoch, start with 0 and return lowest location number, that corresponds to a valid seed
    min_seed = 0
    while True:
        tmp_seed = min_seed
        for m in map_order:
            tmp_seed = inverse_change_me(map_dict[m], tmp_seed)

        # Check if the seed is in a valid range
        for range_start, range_len in pairs:
            if range_start <= tmp_seed < range_start + range_len:
                return min_seed
        min_seed += 1


# Thanks to reddit for the idea of inverse mapping :)
# Gets a mapping from target value to correct index in source
def inverse_change_me(map_strings, target_value):
    for dest_start, source_start, range_len in map_strings:
        # Inverse dest_start and source_start for reverse mapping
        if dest_start <= target_value < dest_start + range_len - 1:
            return source_start + (target_value - dest_start)

    return target_value


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
