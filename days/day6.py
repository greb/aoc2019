import collections

def parse(inp):
    orbits = collections.defaultdict(list)
    for line in inp.splitlines():
        a, b = line.split(')')
        orbits[a].append(b)
    return orbits


def part1(inp):
    orbits = parse(inp)
    cnt = 0
    stack = [(0, 'COM')]
    while stack:
        n, body = stack.pop()
        cnt += n
        for sub_body in orbits[body]:
            stack.append((n+1, sub_body))
    return cnt

def find_path(node, parents):
    path = []
    while node in parents:
        parent = parents[node]
        path.append(parent)
        node = parent
    return path

def part2(inp):
    orbits = parse(inp)

    parents = dict()
    for body, sub_bodies in orbits.items():
        for sub_body in sub_bodies:
            parents[sub_body] = body

    path_you = find_path('YOU', parents)
    path_san = find_path('SAN', parents)

    for body in path_you:
        if body in path_san:
            break

    return path_you.index(body) + path_san.index(body)
