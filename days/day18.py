import collections
import heapq

def parse(inp):
    grid = inp.splitlines()
    start = None
    tiles = dict()
    n_keys = 0
    for y, line in enumerate(grid):
        for x, tile in enumerate(line):
            if tile == '@':
                start = (x,y)
            elif tile.islower():
                n_keys += 1
            tiles[(x,y)] = tile
    return start, tiles, n_keys

def generate_neighbors(tiles):
    neighs = collections.defaultdict(list)
    for pos, tile in tiles.items():
        x, y = pos
        ns = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]
        for n in ns:
            if tiles.get(n, '#') == '#':
                continue
            neighs[pos].append(n)
    return neighs

def reachable_keys(pos, tiles, neighs, keys):
    visited = set()
    visited.add(pos)
    queue = collections.deque()
    queue.appendleft((0, pos))
    found = []

    while queue:
        dist, pos = queue.pop()
        tile = tiles[pos]
        if tile.islower() and tile not in keys:
            found.append((dist, pos, tile))
            continue

        for n_pos in neighs[pos]:
            if n_pos in visited:
                continue
            visited.add(n_pos)
            tile = tiles[n_pos]
            if tile.isupper() and tile.lower() not in keys:
                continue
            queue.appendleft((dist+1, n_pos))
    return found

def shortest_path(start, tiles, n_keys):
    node = tuple(start), frozenset()
    visited = set()
    queue = []
    heapq.heappush(queue, (0, node))
    neighs = generate_neighbors(tiles)

    while queue:
        dist, (pos, keys) = heapq.heappop(queue)
        if len(keys) == n_keys:
            break
        if (pos, keys) in visited:
            continue
        visited.add((pos, keys))

        for i, p in enumerate(pos):
            r_keys = reachable_keys(p, tiles, neighs, keys)
            for k_dist, k_pos, key in r_keys:
                new_pos = pos[:i] + (k_pos,) + pos[i+1:]
                new_keys = keys | frozenset([key])
                node = new_pos, new_keys
                heapq.heappush(queue, (dist + k_dist, node))
    return dist


def part1(inp):
    start, tiles, n_keys = parse(inp)
    return shortest_path([start], tiles, n_keys)

def part2(inp):
    start, tiles, n_keys = parse(inp)

    x,y = start
    for pos in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
        tiles[pos] = '#'
    start = []
    for pos in [(x+1,y+1), (x-1,y+1), (x+1,y-1), (x-1,y-1)]:
        start.append(pos)

    return shortest_path(start, tiles, n_keys)
