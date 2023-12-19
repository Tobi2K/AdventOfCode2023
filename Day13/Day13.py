import numpy as np


def get_patterns_and_transpose(inp):
    patterns = []
    patterns_transpose = []
    cur_pat = []

    for line in inp:
        if line != "":
            cur_pat.append(list(line))
        else:
            patterns.append(cur_pat)
            patterns_transpose.append(np.transpose(cur_pat))
            cur_pat = []
    patterns.append(cur_pat)
    patterns_transpose.append(np.transpose(cur_pat))

    return patterns, patterns_transpose


def first_task(inp):
    patterns, patterns_transpose = get_patterns_and_transpose(inp)

    reflection_summary = 0

    for pats, mult in [(patterns, 100), (patterns_transpose, 1)]:
        for pattern in pats:
            # Skip first row/col, as we always compare to previous row/col
            for idx in list(range(1, len(pattern))):
                # Check if current row/col and row/col before are equal
                if np.array_equal(pattern[idx - 1], pattern[idx]):
                    # If they match, check if they match perfectly
                    if check_perfect(pattern, idx):
                        reflection_summary += mult * idx
                        break

    return reflection_summary


# reflection_idx is the HIGHER index of the two reflected rows
def check_perfect(rows, reflection_idx):
    delta = 1
    while reflection_idx - 1 - delta >= 0 and reflection_idx + delta < len(rows):
        # Check if arrays are exactly equal, if not, return False
        if not np.array_equal(
            rows[reflection_idx - 1 - delta], rows[reflection_idx + delta]
        ):
            return False
        delta += 1
    # We reached a border without conflicts --> Perfect reflection
    return True


def second_task(inp):
    patterns, patterns_transpose = get_patterns_and_transpose(inp)

    refl_idxs = [(-1, -1)] * len(patterns)

    # Get all original reflection axis ids, so we don't use the same row again
    for refl_id, (pattern_row, pattern_col) in enumerate(
        zip(patterns, patterns_transpose)
    ):
        for idx in list(range(1, len(pattern_row))):
            if np.array_equal(pattern_row[idx - 1], pattern_row[idx]):
                if check_perfect(pattern_row, idx):
                    refl_idxs[refl_id] = (idx, -1)
        for idx in list(range(1, len(pattern_col))):
            if np.array_equal(pattern_col[idx - 1], pattern_col[idx]):
                if check_perfect(pattern_col, idx):
                    refl_idxs[refl_id] = (-1, idx)

    reflection_summary = 0
    for pats, tuple_id, multiplicator in [
        (patterns, 0, 100),
        (patterns_transpose, 1, 1),
    ]:
        # Go through pattern array (first non-transposed, i.e., rows, then transposed, i.e., cols)
        for refl_id, pattern in enumerate(pats):
            # Skip first row/col, as we always compare to previous row/col
            for idx in list(range(1, len(pattern))):
                # If this is the row/col we reflected on previously, skip it
                if idx == refl_idxs[refl_id][tuple_id]:
                    continue
                # Get Boolean array of char matches
                truthy_arr = np.compare_chararrays(
                    pattern[idx - 1], pattern[idx], "==", True
                )
                # Count how many chars DO NOT match
                false_count = np.size(truthy_arr) - np.count_nonzero(truthy_arr)
                # If 0 or 1 chars don't match, check if we find a perfect match with just one wrong char
                if false_count < 2:
                    # All reflections matched, with only one wrong char in total
                    if check_close_perfect(pattern, idx, false_count):
                        reflection_summary += multiplicator * idx
                        break

    return reflection_summary


# reflection_idx is the HIGHER index of the two reflected rows
# Here we additionally have a `close_rows` count. Allows rows to have one char difference
def check_close_perfect(rows, reflection_idx, close_rows):
    delta = 1
    while reflection_idx - 1 - delta >= 0 and reflection_idx + delta < len(rows):
        truthy_arr = np.compare_chararrays(
            rows[reflection_idx - 1 - delta], rows[reflection_idx + delta], "==", True
        )
        false_count = np.size(truthy_arr) - np.count_nonzero(truthy_arr)
        # If strings match exactly, continue
        if false_count == 0:
            delta += 1
            continue
        # If strings are one-off, add one to counter
        elif false_count == 1:
            close_rows += 1
        # More than one difference, definitely not a reflection
        else:
            return False
        # Too many one-off rows
        if close_rows > 1:
            return False
        delta += 1
    # We reached a border without conflicts --> Perfect reflection
    return True


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
