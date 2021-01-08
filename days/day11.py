from . import intcode

dirs = {
    'N': (0,-1),
    'E': (1,0),
    'S': (0, 1),
    'W': (-1, 0),
}

turn_r = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N',
}

turn_l = {
    'N': 'W',
    'E': 'N',
    'S': 'E',
    'W': 'S',
}

def forward(pos, dir):
    x,y = pos
    dx,dy = dirs[dir]
    return x+dx, y+dy

def pain_panels(brain, first_panel=0):
    panels = dict()
    pos = (0,0)
    dir = 'N'

    panels[pos] = first_panel

    while brain.is_running():
        color = panels.setdefault(pos, 0)
        brain.send(color)
        brain.run()

        color = brain.recv()
        turn  = brain.recv()
        panels[pos] = color

        dir = turn_r[dir] if turn else turn_l[dir]
        pos = forward(pos, dir)
    return panels

def part1(inp):
    brain = intcode.Machine(inp)
    panels = pain_panels(brain)
    return len(panels)

def part2(inp):
    brain = intcode.Machine(inp)
    panels = pain_panels(brain, first_panel=1)

    xs = [p[0] for p in panels]
    ys = [p[1] for p in panels]

    for y in range(min(ys), max(ys)+1):
        row = []
        for x in range(min(xs), max(xs)+1):
            panel = panels.get((x,y), 0)
            row.append('.#'[panel])
        print(''.join(row))

    # Here should you put your own solution
    return 'KLCZAEGU'
