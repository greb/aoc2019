from . import intcode

import pdb

dirs = '^>v<'

def move(pos, d):
    d = [(0,-1), (1,0), (0,1),(-1,0)][d]
    return tuple(p+d for p,d in zip(pos, d))

def parse_scaffold(prog):
    grid = set()
    robot = None
    for y, line in enumerate(prog.read_lines()):
        if not line:
            break
        for x, tile in enumerate(line):
            if tile != '.':
                grid.add((x,y))
            if tile in dirs:
                robot = (x,y), dirs.index(tile)
    return grid, robot, x+1, y+1

def get_intersections(scaffold):
    grid, _, width, height = scaffold
    intersections = []
    for x in range(1,width-1):
        for y in range(1,height-1):
            pos = (x,y)
            neighs = (move(pos, d) in grid for d in range(4) )
            if pos in grid and all(neighs):
                intersections.append(pos)
    return intersections


def part1(inp):
    prog = intcode.Machine(inp, iomode=intcode.IOMode.TXT)
    scaffold = parse_scaffold(prog)
    return sum(x*y for x,y in get_intersections(scaffold))

def find_path(scaffold):
    grid, robot, _, _ = scaffold
    pos, dir = robot
    visited = set()
    visited.add(pos) # robot start

    path = []
    while visited != grid:
        new_dirs = {
            'F': dir,
            'R': (dir+1) % 4,
            'L': (dir-1) % 4,
            'B': (dir+2) % 4,
        }
        # Random orientation at start?
        cmds = 'RL' if len(path) else 'FRLB'
        for cmd in cmds:
            n_dir = new_dirs[cmd]
            n = 0
            while True:
                n_pos = move(pos, n_dir)
                if n_pos not in grid:
                    break
                pos = n_pos
                visited.add(n_pos)
                n += 1
            if n > 0:
                if cmd in 'RL':
                    path.append(cmd)
                elif cmd == 'B':
                    path.extend('RR')
                path.append(str(n))
                dir = n_dir
                break
    return path


part_max_len = 20
def find_program(path, order=[], seqs=[]):
    if len(seqs) > 3:
        return None

    if len(path) == 0:
        routine = ','.join('ABC'[s] for s in order)
        functions = [','.join(seq) for seq in seqs]
        return [routine] + functions

    # Substract any found sequences
    for s, seq in enumerate(seqs):
        l = len(seq)
        if path[:l] == seq:
            res = find_program(path[l:], order+[s], seqs)
            if res:
                return res

    # Find next sequence
    for i in reversed(range(1, len(path))):
        seq = path[:i]
        if len(','.join(seq)) > 20:
            continue

        res = find_program(path[i:], order + [len(seqs)], seqs + [seq])
        if res:
            return res

def part2(inp):
    prog = intcode.Machine(inp, iomode=intcode.IOMode.TXT)
    prog.store(0, 2)
    scaffold = parse_scaffold(prog) # ignore prompt
    path = find_path(scaffold)
    program = find_program(path)

    for line in program:
        prog.write(line)
        prog.write('\n')
    prog.write('n\n')

    # Consume lines to keep program running
    for line in prog.read_lines():
        pass

    return prog.read(iomode=intcode.IOMode.RAW)[-1]
