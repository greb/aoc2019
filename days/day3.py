def parse(inp):
    wires = []
    for line in inp.splitlines():
        wire = []
        for s in line.split(','):
            wire.append((s[0], int(s[1:])))
        wires.append(wire)
    return wires

def trace_path(wire):
    dirs = {
        'U': (0, -1),
        'R': (1, 0),
        'D': (0, 1),
        'L': (-1, 0)
    }
    points = {}
    dist = 0
    x, y = (0,0)
    for d, steps in wire:
        dx,dy = dirs[d]
        for _ in range(steps):
            dist += 1
            x += dx
            y += dy
            if (x,y) not in points:
                points[(x,y)] = dist
    return points


def part1(inp):
    wires = parse(inp)

    points0 = trace_path(wires[0])
    points1 = trace_path(wires[1])

    # LOL, this set operation is literally called intersection
    intersections = points0.keys() & points1.keys()
    return min(abs(a)+abs(b) for a,b in intersections)


def part2(inp):
    wires = parse(inp)

    points0 = trace_path(wires[0])
    points1 = trace_path(wires[1])

    intersections = points0.keys() & points1.keys()
    return min(points0[p] + points1[p] for p in intersections)
