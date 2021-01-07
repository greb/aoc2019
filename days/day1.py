def fuel_needed(mass):
    return (mass//3) - 2


def fuel_needed2(mass):
    total = 0
    while True:
        mass = mass // 3 - 2
        if mass <= 0:
            break
        total += mass
    return total

def part1(inp):
    modules = [int(m) for m in inp.splitlines()]
    return sum(fuel_needed(m) for m in modules)

def part2(inp):
    modules = [int(m) for m in inp.splitlines()]
    return sum(fuel_needed2(m) for m in modules)
