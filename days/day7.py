from . import intcode

import itertools

def part1(inp):
    amps = [intcode.Machine(inp) for _ in range(5)]

    best_signal = 0
    for perm in itertools.permutations(range(5)):
        signal = 0
        for phase, amp in zip(perm, amps):
            amp.inp_queue.appendleft(phase)
            amp.inp_queue.appendleft(signal)

            amp.run()
            signal = amp.out_queue.pop()
            amp.reset()
        if signal > best_signal:
            best_signal = signal

    return best_signal


def part2(inp):
    amps = [intcode.Machine(inp) for _ in range(5)]

    best_signal = 0
    for perm in itertools.permutations(range(5,10)):
        for phase, amp in zip(perm, amps):
            amp.reset()
            amp.inp_queue.appendleft(phase)

        signal = 0
        halt = False
        while not halt:
            for amp in amps:
                amp.inp_queue.appendleft(signal)
                status = amp.run()
                signal = amp.out_queue.pop()
                if status == intcode.Status.HLT:
                    halt = True
        if signal > best_signal:
            best_signal = signal

    return best_signal
