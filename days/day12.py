import math
import re

def parse(inp):
    moons = []
    for line in inp.splitlines():
        moon = []
        pos = map(int, re.findall(r'-?\d+', line))
        for p in pos:
            moon.append((p,0))
        moons.append(moon)
    # Flip matrix on its axes. We need it later for part2
    return list(m for m in zip(*moons))

def cmp(a,b):
    return int(b>a) - int(b<a)

def time_step(axis):
    new_axis = []
    for i, (p, v) in enumerate(axis):
        for j, (p1,_) in enumerate(axis):
            if i == j:
                continue
            v += cmp(p, p1)
        p += v
        new_axis.append((p, v))
    return tuple(new_axis)

def part1(inp):
    axes = parse(inp)

    new_axes = []
    for axis in axes:
        for _ in range(1000):
            axis = time_step(axis)
        new_axes.append(axis)

    moons = list(a for a in zip(*new_axes))
    energy = 0
    for moon in moons:
        pot, kin = 0, 0
        for p,v in moon:
            pot += abs(p)
            kin += abs(v)
        energy += pot*kin
    return energy

def part2(inp):
    axes = parse(inp)

    periods = []
    for axis in axes:
        original = axis
        idx = 0
        while True:
            axis = time_step(axis)
            idx += 1
            if axis == original:
                break
        periods.append(idx)
    return math.lcm(*periods)
