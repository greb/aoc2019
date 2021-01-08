from . import intcode
import time

def chunked(it, n):
    its = [iter(it)]*n
    return zip(*its)

class Arcade:
    def __init__(self, inp, quarter=False):
        self.cpu = intcode.Machine(inp)
        if quarter:
            self.cpu.store(0,2) # Free play!

        self.screen = dict()
        self.dims = None

        self.score  = 0
        self.blocks = set()
        self.paddle = None
        self.ball = None

        self.update()

    def update(self):
        self.cpu.run()
        out = self.cpu.recv_all()

        for x,y,tile in chunked(out, 3):
            if x < 0:
                self.score = tile
                continue

            self.screen[(x,y)] = ' #*_o'[tile]
            if tile == 2:
                self.blocks.add((x,y))
            elif tile == 3:
                self.paddle = x
            elif tile == 4:
                self.ball = x

            if (x,y) in self.blocks and tile != 2:
                self.blocks.discard((x,y))

        if not self.dims:
            width = max(t[0] for t in self.screen)+1
            height = max(t[1] for t in self.screen)+1
            self.dims = width, height

    def step(self):
        if self.paddle > self.ball:
            self.cpu.send(-1)
        elif self.paddle < self.ball:
            self.cpu.send(1)
        else:
            self.cpu.send(0)
        self.update()

    def print(self):
        width, height = self.dims
        for y in range(height):
            row = []
            for x in range(width):
                row.append(self.screen.get((x,y), 'X'))
            print(''.join(row))
        print(f'Score: {self.score}')
        time.sleep(0.01)

def part1(inp):
    arcade = Arcade(inp)
    #arcade.print()
    return len(arcade.blocks)

def part2(inp):
    arcade = Arcade(inp, True)
    while arcade.blocks:
        arcade.step()
        #arcade.print()
    return arcade.score
