from . import intcode

def part1(inp):
    machine = intcode.Machine(inp)
    machine.inp_queue.appendleft(1)
    machine.run()
    return machine.out_queue[0]

def part2(inp):
    machine = intcode.Machine(inp)
    machine.inp_queue.appendleft(2)
    machine.run()
    return machine.out_queue[0]
