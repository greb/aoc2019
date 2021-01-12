import collections

import pdb

src_portal = 'AA'
dst_portal = 'ZZ'

dirs = (
    ((0,-1), True),
    ((1,0),  False),
    ((0,1),  False),
    ((-1,0), True),
)

def parse(inp):
    grid = inp.splitlines()
    move = lambda p,d: tuple(a+b for a,b in zip(p,d))
    neighs = collections.defaultdict(list)
    portals = collections.defaultdict(list)

    mx = len(grid[0]) -1
    my = len(grid) - 1
    src = None
    dst = None

    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile != '.':
                continue
            for d, rev in dirs:
                nx,ny = move((x,y), d)
                n = grid[ny][nx]
                if n == '.':
                    neighs[(x,y)].append((nx,ny))
                elif n.isupper():
                    # It's a portal
                    nx,ny = move((nx,ny), d)
                    portal = [n, grid[ny][nx]]
                    if rev:
                        portal = ''.join(reversed(portal))
                    else:
                        portal = ''.join(portal)
                    if portal == src_portal:
                        src = (x,y)
                        continue
                    elif portal == dst_portal:
                        dst = (x,y)
                        continue
                    if nx in (0,mx) or ny in (0,my):
                        outer = True
                    else:
                        outer = False
                    portals[portal].append(((x,y), outer))
                    neighs[(x,y)].append(portal)

    for pos, neigh in neighs.items():
        new_neigh = []
        for n in neigh:
            portal = portals.get(n)
            if portal:
                n, outer = portal[1] if portal[0][0] == pos else portal[0]
                # switch inner and outer
                new_neigh.append((n, not outer)) 
            else:
                new_neigh.append((n, None))
        neighs[pos] = new_neigh

    return src, dst, neighs

def part1(inp):
    src, dst, neighs = parse(inp)
    visited = set([src])
    queue = collections.deque([(0, src)])

    while queue:
        dist, pos = queue.pop()
        if pos == dst:
            break
        for n_pos, _ in neighs[pos]:
            if n_pos in visited:
                continue
            visited.add(n_pos)
            queue.appendleft((dist+1, n_pos))
    return dist

def part2(inp):
    src, dst, neighs = parse(inp)

    visited = set([(0, src)])
    queue = collections.deque([(0, 0, src)])

    while queue:
        dist, lvl, pos = queue.pop()
        if pos == dst:
            break
        for n_pos, outer in neighs[pos]:
            if lvl == 0 and outer:
                continue
            if lvl > 0 and n_pos in (src, dst):
                continue
            if outer is not None:
                n_lvl = lvl-1 if outer else lvl+1
            else:
                n_lvl = lvl

            if (n_lvl, n_pos) in visited:
                continue
            visited.add((n_lvl, n_pos))
            queue.appendleft((dist+1, n_lvl, n_pos))
    return dist

