import collections

size = 5

def parse(inp):
    bugs = set()
    for y, line in enumerate(inp.splitlines()):
        for x, cell in enumerate(line):
            if cell == '#':
                bugs.add((0, x,y))
    return bugs

def bio_rating(bugs):
    score = 0
    for y in reversed(range(size)):
        for x in reversed(range(size)):
            score <<= 1
            score |= (0, x,y) in bugs
    return score

def neighbors(pos):
    lvl, x, y = pos
    neighs = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
    for nx, ny in neighs:
        if (0 <= nx < size) and (0 <= ny < size):
            yield lvl, nx, ny

def step(bugs, neigh_f):
    new_bugs = set()
    neighs_cnt = collections.defaultdict(int)
    for pos in bugs:
        for neigh in neigh_f(pos):
            neighs_cnt[neigh] += 1

    for pos, cnt in neighs_cnt.items():
        if pos in bugs and cnt == 1:
            new_bugs.add(pos)
        elif pos not in bugs and cnt in (1,2):
            new_bugs.add(pos)
    return new_bugs

def print_bugs(bugs):
    lvls = [b[0] for b in bugs]
    for lvl in range(min(lvls), max(lvls)+1):
        print(f'Level {lvl}')
        for y in range(5):
            row = []
            for x in range(5):
                if (lvl, x, y) in bugs:
                    row.append('#')
                else:
                    row.append('.')
            print(''.join(row))

def part1(inp):
    bugs = parse(inp)
    history = set()
    score = 0

    while score not in history:
        history.add(score)
        bugs = step(bugs, neighbors)
        score = bio_rating(bugs)
    return score


def pluto_neighbors(pos):
    lvl, x, y = pos

    neighs = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
    for nx,ny in neighs:
        if nx == 2 and ny == 2:
            n_lvl = lvl+1
            if y == 2:
                nx = 0 if x == 1 else 4
                yield from ((n_lvl, nx, ny) for ny in range(5))
            if x == 2:
                ny = 0 if y == 1 else 4
                yield from ((n_lvl, nx, ny) for nx in range(5))

        elif not(0 <= nx < size):
            nx = 1 if nx == -1 else 3
            yield lvl-1, nx, 2
        elif not(0 <= ny < size):
            ny = 1 if ny == -1 else 3
            yield lvl-1, 2, ny
        else:
            yield lvl, nx, ny

def part2(inp):
    bugs = parse(inp)
    for _ in range(200):
        bugs = step(bugs, pluto_neighbors)

    return len(bugs)
