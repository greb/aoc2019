from . import intcode

import collections
import itertools
import pdb

def chunks(it, n):
    it = iter(it)
    chunk = tuple(itertools.islice(it, n))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, n))

def gen_nics(inp, n_nics):
    nics = []
    for addr in range(n_nics):
        nic = intcode.Machine(inp)
        nic.write(addr)
        nic.write(-1)
        nics.append(nic)
    return nics

def part1(inp):
    n_nics = 50
    nics = gen_nics(inp, n_nics)

    messages = [list() for _ in range(n_nics)]
    run = True
    while run:
        for src, nic in enumerate(nics):
            nic.run()
            for dst, x, y in chunks(nic.read(), 3):
                if dst == 255:
                    run = False
                    break
                messages[dst].append(x)
                messages[dst].append(y)

        for src, nic in enumerate(nics):
            if messages[src]:
                nic.write(messages[src])
                messages[src] = list()
            else:
                nic.write(-1)

    return y

def part2(inp):
    n_nics = 50
    nics = gen_nics(inp, n_nics)

    messages = [list() for _ in range(n_nics)]
    run = True
    nat = None
    last_nat_y = None
    while run:
        for src, nic in enumerate(nics):
            nic.run()
            for dst, x, y in chunks(nic.read(), 3):
                if dst == 255:
                    nat = (x,y)
                    continue
                messages[dst].append(x)
                messages[dst].append(y)

        idle = all(len(m) == 0 for m in messages)
        if idle:
            if last_nat_y == nat[1]:
                break
            else:
                last_nat_y = nat[1]

        for src, nic in enumerate(nics):
            if messages[src]:
                nic.write(messages[src])
                messages[src] = list()
            elif idle and src == 0:
                nic.write(nat)
            else:
                nic.write(-1)

    return last_nat_y
