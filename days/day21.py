from . import intcode

def part1(inp):
    interpreter = intcode.Machine(inp, iomode=intcode.IOMode.TXT)
    interpreter.run()

    interpreter.write('NOT C J\n')
    interpreter.write('AND D J\n')
    interpreter.write('NOT A T\n')
    interpreter.write('OR T J\n')
    interpreter.write('WALK\n')

    for line in interpreter.read_lines():
        pass
    return interpreter.read(iomode=intcode.IOMode.RAW)[0]

def part2(inp):
    interpreter = intcode.Machine(inp, iomode=intcode.IOMode.TXT)
    interpreter.run()

    interpreter.write('NOT C J\n')
    interpreter.write('AND D J\n')
    interpreter.write('AND H J\n')

    interpreter.write('NOT B T\n')
    interpreter.write('AND D T\n')
    interpreter.write('OR T J\n')

    interpreter.write('NOT A T\n')
    interpreter.write('OR T J\n')
    interpreter.write('RUN\n')

    for line in interpreter.read_lines():
        pass
    return interpreter.read(iomode=intcode.IOMode.RAW)[0]
