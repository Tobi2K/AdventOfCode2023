from collections import deque
from math import lcm


def create_dicts(inp):
    signal_dict = {}

    con = {}
    ff = {}

    # False is a low pulse, True is a high pulse
    for line in inp:
        parts = line.split(" -> ")
        mod_name = parts[0]
        signals = parts[1].split(", ")
        # conjunction module
        if mod_name[0] == "&":
            mod_name = mod_name[1:]
            con[mod_name] = {}
        # flip flop module
        elif mod_name[0] == "%":
            mod_name = mod_name[1:]
            ff[mod_name] = False
        signal_dict[mod_name] = signals
    # Set all inputs of the conjunction module
    for module, signals in signal_dict.items():
        for sig in signals:
            if sig in con:
                con[sig][module] = False

    return signal_dict, con, ff


def first_task(inp):
    signal_dict, con, ff = create_dicts(inp)

    # Find count of high and low pulses after 1000 presses
    hp_count = 0
    lp_count = 0
    for _ in range(1000):
        hp, lp = push_button(signal_dict, con, ff)
        hp_count += hp
        lp_count += lp

    return hp_count * lp_count


# I did not understand how to optimize this. Went to reddit for help.
# Signal to rx comes from a conjunction module (qt)
# Signals to qt also comes from conjunction modules (mr, kk, gl, bb)
# qt sends a low pulse to rx, if mr, kk, gl, bb send low pulses at a time
# find the first time mr, kk, gl, bb send low pulse and compute lcm
def second_task(inp):
    signal_dict, con, ff = create_dicts(inp)

    # Find the module that sends a signal to rx
    to_rx = None
    for source, signals in signal_dict.items():
        if "rx" in signals:
            to_rx = source
    # rx can't be reached
    if not to_rx:
        return "rx can't be reached"

    # Find signals that lead to the module that sends a signal to rx
    signal_steps = []
    for source, signals in signal_dict.items():
        if to_rx in signals:
            signal_steps.append(source)

    # LCM tracker
    lcm_store = 1
    presses = 0
    while True:
        presses += 1
        signal_queue = deque([("button_mod", "broadcaster", False)])
        # simulate one button press
        while len(signal_queue) > 0:
            origin, mod_name, signal = signal_queue.popleft()
            # Low signal
            if not signal:
                # Found a module that sends a signal to module before rx
                if mod_name in signal_steps:
                    # Update lcm
                    lcm_store = lcm(lcm_store, presses)
                    # Remove signal from tracker
                    signal_steps.remove(mod_name)
                    # If we have no signal left, we found all signals that send to rx input module
                    if len(signal_steps) == 0:
                        return lcm_store

            new_signals = send_pulse(signal_dict, con, ff, origin, mod_name, signal)
            if new_signals:
                for sig in new_signals:
                    signal_queue.append(sig)


def push_button(signal_dict, con, ff):
    hp_count = 0
    lp_count = 0

    signal_queue = deque([("button_mod", "broadcaster", False)])

    while len(signal_queue) > 0:
        origin, mod_name, signal = signal_queue.popleft()
        # add to counter depending on the high or low pulse
        if signal:
            hp_count += 1
        else:
            lp_count += 1
        # get next pulses
        new_signals = send_pulse(signal_dict, con, ff, origin, mod_name, signal)
        if new_signals:
            for sig in new_signals:
                signal_queue.append(sig)

    return hp_count, lp_count


def send_pulse(signal_dict, con, ff, origin, mod_name, signal):
    # Our current module is a conjunction
    if mod_name in con:
        # Set the input of the origin
        con[mod_name][origin] = signal
        # Check if all inputs have the same state
        send_pulse = not all(con[mod_name].values())
    # Our current module is a flip-flop
    elif mod_name in ff:
        # received a high pulse --> ignore
        if signal:
            return
        # Send the inverse of the current signal to the destinations
        send_pulse = not ff[mod_name]
        # Flip the flip-flop
        ff[mod_name] = not ff[mod_name]
    # Some other module (should be broadcaster)
    elif mod_name in signal_dict:
        send_pulse = signal
    else:
        return

    new_signal = []
    for sig in signal_dict[mod_name]:
        new_signal.append((mod_name, sig, send_pulse))

    return new_signal


def main(test_inp, task_inp):
    print("First Task, Test Input:\t\t", first_task(test_inp))
    print("First Task, Task Input:\t\t", first_task(task_inp))
    print("Second Task, Test Input:\t", second_task(test_inp))
    print("Second Task, Task Input:\t", second_task(task_inp))
