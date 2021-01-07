import re
import itertools


def part1(inp):
    a, b = map(int, inp.strip().split('-'))
    cnt = 0

    for n in range(a,b+1):
        s = str(n)
        sort = ''.join(sorted(s))
        if s != sort:
            continue

        cnt_doubles = 0
        for _, g in itertools.groupby(sort):
            if len(list(g)) >= 2:
                cnt_doubles += 1
        if not cnt_doubles:
            continue
        cnt += 1
    return cnt

def part2(inp):
    a, b = map(int, inp.strip().split('-'))
    cnt = 0

    for n in range(a,b+1):
        s = str(n)
        sort = ''.join(sorted(s))
        if s != sort:
            continue

        cnt_doubles = 0
        for _, g in itertools.groupby(sort):
            if len(list(g)) == 2:
                cnt_doubles += 1
        if not cnt_doubles:
            continue
        cnt += 1
    return cnt


