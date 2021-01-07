import itertools

from . import intcode

def run_assist(machine, noun, verb):
    machine.reset()
    machine.store(1,noun)
    machine.store(2,verb)
    machine.run()
    return machine.load(0)


def part1(inp):
    machine = intcode.Machine(inp)
    return run_assist(machine, 12, 2)


def part2(inp):
    machine = intcode.Machine(inp)
    target_val = 19690720

    for noun, verb in itertools.product(range(0, 100), repeat=2):
        val = run_assist(machine, noun, verb)
        if val == target_val:
            break

    return 100 * noun + verb
