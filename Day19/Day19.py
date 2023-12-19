import copy
import math
import re


def get_ratings_and_workflows(inp):
    # Save workflow as a dict with entries as "wf_id": {"rules": [{"cat": "x|m|a|s", "op": "<|>", "value": int, "next": <wf_id>|"R"|"S"}, ...], "last": <wf_id>|"R"|"S"}
    workflow_dict = dict()
    # Save ratings as array of dicts with {"x": int, "m": int, "a": int, "s": int}
    ratings = []
    # If we should start parsing ratings of parts
    parse_parts = False
    for line in inp:
        # found empty line ==> Parse ratings next
        if line == "":
            parse_parts = True
            continue
        if not parse_parts:
            # Match string and save according to structure above
            workflow = re.search(r"([a-z]+)\{(.+)\}", line)
            w_name = workflow.group(1)
            w_rules = workflow.group(2).split(",")
            w_last = w_rules[-1]
            w_rules = w_rules[:-1]
            parsed_rules = []
            for rule in w_rules:
                p_rule = re.search(r"([a-z])(\>|\<)(\d+)\:([a-zA-Z]+)", rule)
                category = p_rule.group(1)
                operator = p_rule.group(2)
                value = int(p_rule.group(3))
                next_step = p_rule.group(4)
                parsed_rules.append(
                    {"cat": category, "op": operator, "value": value, "next": next_step}
                )

            workflow_dict[w_name] = {"rules": parsed_rules, "last": w_last}
        else:
            # Match string and save according to structure above
            rates = re.search(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", line)
            ratings.append(
                {
                    "x": int(rates.group(1)),
                    "m": int(rates.group(2)),
                    "a": int(rates.group(3)),
                    "s": int(rates.group(4)),
                }
            )

    return workflow_dict, ratings


def first_task(inp):
    workflow_dict, ratings = get_ratings_and_workflows(inp)
    accepted_parts = []

    for rate in ratings:
        current_wf = "in"
        while True:
            # Get our current workflow
            workflow = workflow_dict[current_wf]
            found_match = False
            for rule in workflow["rules"]:
                # Get parts
                op = rule["op"]
                val = rule["value"]
                cat = rule["cat"]
                if op == "<":
                    if rate[cat] < val:
                        # If this rule was matched, continue to next workflow
                        current_wf = rule["next"]
                        found_match = True
                        break
                elif op == ">":
                    if rate[cat] > val:
                        # If this rule was matched, continue to next workflow
                        current_wf = rule["next"]
                        found_match = True
                        break
            # If we haven't found a match in our rule, go to last option
            if not found_match:
                current_wf = workflow["last"]

            # Do not accept, i.e. break while loop and continue with next rating
            if current_wf == "R":
                break
            # Accept part, add it to our set
            if current_wf == "A":
                accepted_parts.append(rate)
                break
    # Sum the values of all accepted parts
    part_sum = 0
    for part in accepted_parts:
        for i in part.values():
            part_sum += i
    return part_sum


def second_task(inp):
    # We only need the workflow
    workflow_dict, _ = get_ratings_and_workflows(inp)

    return calculate_possible_combinations(
        workflow_dict,
        "in",
        {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)},
    )


def calculate_possible_combinations(workflow_dict, workflow_name, ranges):
    if workflow_name == "R":
        # Return 0 if our workflow was rejected
        return 0
    elif workflow_name == "A":
        # Calculate product of all ranges that achieved an 'accept' state
        return math.prod(
            (range_end - range_start + 1) for range_start, range_end in ranges.values()
        )
    combinations = 0
    # Get workflow details
    workflow = workflow_dict[workflow_name]
    for rule in workflow["rules"]:
        # Get current bounds for operator
        cur_lower, cur_upper = ranges[rule["cat"]]
        if rule["op"] == ">":
            copy_range_lower = copy.deepcopy(ranges)
            copy_range_upper = copy.deepcopy(ranges)
            # Range that does not fulfill condition --> save as current range and continue
            copy_range_lower[rule["cat"]] = (cur_lower, rule["value"])
            # Range that fulfills condition --> Continue with 'next' workflow
            copy_range_upper[rule["cat"]] = (rule["value"] + 1, cur_upper)

            ranges = copy_range_lower

            # Add the combinations that we achieve if we 'branch off' from our current part
            combinations += calculate_possible_combinations(
                workflow_dict, rule["next"], copy_range_upper
            )
        elif rule["op"] == "<":
            copy_range_lower = copy.deepcopy(ranges)
            copy_range_upper = copy.deepcopy(ranges)
            # Range that fulfills condition --> Continue with 'next' workflow
            copy_range_lower[rule["cat"]] = (cur_lower, rule["value"] - 1)
            # Range that does not fulfill condition --> save as current range and continue
            copy_range_upper[rule["cat"]] = (rule["value"], cur_upper)

            ranges = copy_range_upper

            # Add the combinations that we achieve if we 'branch off' from our current part
            combinations += calculate_possible_combinations(
                workflow_dict, rule["next"], copy_range_lower
            )
        else:
            raise Exception("Illegal operator received")

    # Add combinations for the last step in our workflow
    return combinations + calculate_possible_combinations(
        workflow_dict, workflow["last"], ranges
    )


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
