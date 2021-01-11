from . import intcode

import pdb

MAX_X = 10_000
MAX_Y = 10_000

def get_pull(tractor, x, y):
    tractor.write([x,y])
    tractor.run()
    result = tractor.out_queue.pop()
    tractor.reset()
    return result

def part1(inp):
    tractor = intcode.Machine(inp, memsize=512)

    cnt = 0
    for y in range(50):
        row = []
        for x in range(50):
            cnt += get_pull(tractor, x, y)
    return cnt

def part2(inp):
    tractor = intcode.Machine(inp, memsize=512)
    size = 100

    y = 0
    x = 0
    while True:
        while True:
            test_y = y + (size-1)
            if get_pull(tractor, x, test_y):
                break
            x += 1

        test_x = x + (size-1)
        if get_pull(tractor, test_x, y):
            break
        y += 1

    return x*10_000 + y
