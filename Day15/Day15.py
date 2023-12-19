def first_task(inp):
    # Split on ,
    split_parts = inp[0].split(",")
    init_sum = 0

    # Calculate and sum hashes for each part
    for part in split_parts:
        init_sum += hash_me(part)

    return init_sum


def second_task(inp):
    # Create a dict for each box
    # Python Dicts (in Python 3.7) are ordered, so we can simply add items and they will be ordered by insertion time
    lens_dicts = [dict() for _ in range(256)]

    split_parts = inp[0].split(",")
    for part in split_parts:
        # If part contains =, add a lens
        if "=" in part:
            # Split to get label and focal length
            splits = part.split("=")
            label = splits[0]
            focal_length = int(splits[1])
            # Get label hash
            label_hash = hash_me(label)

            # Add (or overwrite) the focal length of current label
            lens_dicts[label_hash][label] = focal_length
        elif "-" in part:
            # Split to get label and calculate hash
            splits = part.split("-")
            label = splits[0]
            label_hash = hash_me(label)
            # If label is present, delete it from dict
            if label in lens_dicts[label_hash]:
                del lens_dicts[label_hash][label]

    # Go through (ordered) dicts and calculate lens configuration
    config_sum = 0
    for idx, d in enumerate(lens_dicts):
        for jdx, c in enumerate(d):
            config_sum += (idx + 1) * (jdx + 1) * d[c]

    return config_sum


# Calculate the hash value of a string
def hash_me(part):
    current_value = 0
    for c in part:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
