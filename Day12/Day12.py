import sys
from functools import cache
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from AdventOfCode2023.utils import get_file_as_lines  # noqa: E402

FOLDER = "Day12/"

def first_task(path):
    inp = get_file_as_lines(path)
    
    spring_noisy = []
    spring_pairing =[]
    for line in inp:
        line = line.split(" ")
        spring_noisy.append(line[0])
        spring_pairing.append([int(x) for x in line[1].split(",")])
        
    combination_sum = 0
    for noisy_config, grouped_config in zip(spring_noisy, spring_pairing):
        combination_sum += combinations(noisy_config, grouped_config)
        
    return combination_sum

def combinations(noisy_config, grouped_config):
    count = 0
    # We don't have anything left to divide up
    if not grouped_config:
        # Remaining config is not valid
        if "#" in noisy_config:
            return 0
        # Else, we have nothing more to permute, so one combination left
        return 1
    # I'm stupid. This simple check took me an hour to figure out that it was missing
    if len(noisy_config) < grouped_config[0]:
        return 0
    # If we do not have a . in the first part of the config (i.e. only # and ? in the leading section determined by grouped_config[0])
    if "." not in noisy_config[:grouped_config[0]]:
        # If we can exactly match our first group on the noisy config (and it only contains # and ?), cut the noisy config by that amount and remove first element of grouped config and call method recursively
        if len(noisy_config) == grouped_config[0]:
            count += combinations(noisy_config[grouped_config[0] + 1:], grouped_config[1:])
        # If the first spot after we would apply our first group is not a #, we also recursively call
        # If it were a #, then the config would not be valid, because we would be splitting a series of #s
        elif noisy_config[grouped_config[0]] != "#":
            count += combinations(noisy_config[grouped_config[0] + 1:], grouped_config[1:])
    # If we do not start with a "#", start one spot later
    # With this we simplify removing leading non-#s
    if noisy_config[0] != "#":
        count += combinations(noisy_config[1:], grouped_config)
    
    return count
            
    

def second_task(path):
    inp = get_file_as_lines(path)
    
    spring_noisy = []
    spring_pairing =[]
    for line in inp:
        line = line.split(" ")
        tmp = tuple([int(x) for x in line[1].split(",")])
        s_noisy = line[0]
        s_pairing = tuple([int(x) for x in line[1].split(",")])
        for _ in range(4):
            s_noisy += "?" + line[0]
            s_pairing += tmp
        spring_noisy.append(s_noisy)
        spring_pairing.append(s_pairing)
    combination_sum = 0
    for config_tuple in zip(spring_noisy, spring_pairing):
        combination_sum += combinations_cached(config_tuple)
        
    return combination_sum

# First task runs perfectly without cache, test input for second task as well. Second part, task input takes ages w/o caching (thanks reddit, again, for simple package recommendation)
# NOTE: We cannot use lists when caching --> Tuple conversion in `second_task`
@cache
def combinations_cached(config_tuple):
    noisy_config, grouped_config = config_tuple
    count = 0
    # We don't have anything left to divide up
    if not grouped_config:
        # Remaining config is not valid
        if "#" in noisy_config:
            return 0
        # Else, we have nothing more to permute, so one combination left
        return 1
    # I'm stupid. This simple check took me an hour to figure out that it was missing
    if len(noisy_config) < grouped_config[0]:
        return 0
    # If we do not have a . in the first part of the config (i.e. only # and ? in the leading section determined by grouped_config[0])
    if "." not in noisy_config[:grouped_config[0]]:
        # If we can exactly match our first group on the noisy config (and it only contains # and ?), cut the noisy config by that amount and remove first element of grouped config and call method recursively
        if len(noisy_config) == grouped_config[0]:
            count += combinations_cached((noisy_config[grouped_config[0] + 1:], grouped_config[1:]))
        # If the first spot after we would apply our first group is not a #, we also recursively call
        # If it were a #, then the config would not be valid, because we would be splitting a series of #s
        elif noisy_config[grouped_config[0]] != "#":
            count += combinations_cached((noisy_config[grouped_config[0] + 1:], grouped_config[1:]))
    # If we do not start with a "#", start one spot later
    # With this we simplify removing leading non-#s
    if noisy_config[0] != "#":
        count += combinations_cached((noisy_config[1:], grouped_config))
    
    return count
            


if __name__ == "__main__":
    print("First Task, Test Input:\t\t", first_task(FOLDER + "test-input.txt"))
    print("First Task, Task Input:\t\t", first_task(FOLDER + "input.txt"))
    print("Second Task, Test Input:\t", second_task(FOLDER + "test-input.txt"))
    print("Second Task, Task Input:\t", second_task(FOLDER + "input.txt"))