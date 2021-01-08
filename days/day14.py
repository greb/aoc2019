import pdb

def parse_chem(chem):
    n, chem = chem.split()
    return int(n), chem

def parse(inp):
    reactions = dict()
    for line in inp.splitlines():
        inp, out_chem = line.split(' => ')
        out_n, out_chem = parse_chem(out_chem)
        in_chems = [parse_chem(in_chem) for in_chem in inp.split(', ')]
        reactions[out_chem] = (out_n, in_chems)
    return reactions

def ore_needed(fuel, reactions):
    ore = 0
    stack = [(fuel, 'FUEL')]
    reserves = dict()

    while stack:
        out_need, out_chem = stack.pop()
        if out_chem == 'ORE':
            ore += out_need
            continue
        avail = reserves.setdefault(out_chem, 0)
        consumed = min(out_need, avail)
        out_need -= consumed
        reserves[out_chem] -= consumed

        out_n, inps = reactions[out_chem]
        inp_need, shortage = divmod(out_need, out_n)
        if shortage:
            inp_need += 1
            reserves[out_chem] += out_n - shortage

        for inp_n, inp_chem in inps:
            stack.append((inp_need*inp_n, inp_chem))
    return ore


def part1(inp):
    reactions = parse(inp)
    return ore_needed(1, reactions)

def part2(inp):
    reactions = parse(inp)

    ore_avail = 1_000_000_000_000 # ONE TRILLION!!!
    lo = ore_avail // ore_needed(1, reactions)
    hi = lo*2

    # Binary seach
    while lo+1 < hi:
        mid = (lo+hi) // 2
        ore = ore_needed(mid, reactions)
        if ore > ore_avail:
            hi = mid
        else:
            lo = mid
    return lo
