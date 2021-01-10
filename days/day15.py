import collections

from . import intcode

dirs = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]

def move(pos, dir):
    x, y = pos
    dx, dy = dirs[dir]
    return x+dx, y+dy

def control_robot(control, dir):
    control.write(dir+1)
    control.run()
    return control.read()[0]

def map_maze(control):
    oxygen = None
    maze   = dict()
    pos = (0,0)
    maze[pos] = 1
    stack = []

    # Strange DFS, but reduces movements of robot
    while True:
        for dir in range(len(dirs)):
            n_pos = move(pos, dir)
            if n_pos in maze:
                continue

            status = control_robot(control, dir)
            maze[n_pos] = status
            if status == 0:
                continue

            if status == 2:
                oxygen = n_pos

            rev_dir = dir^0x1
            stack.append((pos, rev_dir))
            pos = n_pos
            break
        else:
            # Neighborhood checked, backtrack
            if not stack:
                break
            pos, rev_dir = stack.pop()
            control_robot(control, rev_dir)
    return maze, oxygen

def print_maze(maze):
    xs = [c[0] for c in maze]
    ys = [c[1] for c in maze]

    for y in range(min(ys), max(ys)+1):
        row = []
        for x in range(min(xs), max(xs)+1):
            t = maze.get((x,y), 3)
            row.append('# O.'[t])
        print(''.join(row))


def shortest_dist(maze, src, dest=None):
    dists = {src: 0}
    queue = collections.deque()
    queue.appendleft(src)
    while queue:
        pos = queue.pop()
        if dest and pos == dest:
            return dists[pos]

        for d in range(len(dirs)):
            n_pos = move(pos, d)
            if maze.get(n_pos, 0) == 0:
                continue

            if n_pos not in dists:
                dists[n_pos] = dists[pos] + 1
                queue.appendleft(n_pos)
    return dists

def part1(inp):
    control = intcode.Machine(inp)
    maze, oxygen = map_maze(control)
    return shortest_dist(maze, (0,0), oxygen)

def part2(inp):
    control = intcode.Machine(inp)
    maze, oxygen = map_maze(control)
    dists = shortest_dist(maze, oxygen)
    return max(dists.values())

