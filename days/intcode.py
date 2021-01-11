import enum
import collections
import pdb

class ExecutionError(Exception):
    pass

class MemoryAccessError(Exception):
    pass

class OpError(Exception):
    pass

class Status(enum.Enum):
    RUN = 'run'
    HLT = 'halt'
    WFI = 'wait for input'
    RDY = 'line ready'

class IOMode(enum.Enum):
    RAW = 'Raw I/O'
    TXT = 'Text IO'

def parse_code(code):
    if code is None:
        return []
    elif isinstance(code, list):
        return code
    elif isinstance(code, str):
        return [int(c) for c in code.strip().split(',')]
    else:
        raise ValueError('Invalid code')

class Machine:
    def __init__(self, code, iomode=IOMode.RAW, memsize=None):
        self.rom = parse_code(code)
        self.iomode = iomode
        if not memsize:
            # Should be enough for anyone
            self.memsize = 640 * 1024
        else:
            self.memsize = memsize
        assert self.memsize >= len(self.rom)

        self.reset()
        self.opcodes = {
            1: self.op_add,
            2: self.op_mul,
            3: self.op_inp,
            4: self.op_out,
            5: self.op_jit,
            6: self.op_jif,
            7: self.op_lt,
            8: self.op_eq,
            9: self.op_adj,
            99: self.op_hlt
        }

    def reset(self):
        self.instr_pointer = 0
        self.relative_base = 0

        self.status = Status.RUN
        self.modes = (0,0,0)

        self.memory = [0]*self.memsize
        for addr, val in enumerate(self.rom):
            self.memory[addr] = val

        self.inp_queue = collections.deque()
        self.out_queue = collections.deque()

    def run(self):
        while True:
            self.step()
            if self.status != Status.RUN:
                break
        return self.status

    def is_running(self):
        return self.status != Status.HLT

    def write(self, data):
        if self.iomode == IOMode.RAW:
            if isinstance(data, bool):
                self.inp_queue.appendleft(int(data))
            elif isinstance(data, int):
                self.inp_queue.appendleft(data)
            elif isinstance(data, collections.abc.Iterable):
                self.inp_queue.extendleft(data)
            else:
                raise ValueError('Invalid input data for raw mode')

        elif self.iomode == IOMode.TXT:
            if isinstance(data, str):
                data = map(ord, data)
                self.inp_queue.extendleft(data)
            else:
                raise ValueError('Invalid input data for text mode')


    def read(self, n=None, iomode=None):
        if n is None:
            n = len(self.out_queue)
        iomode = iomode if iomode else self.iomode

        out = []
        for _ in range(n):
            out.append(self.out_queue.pop())

        if iomode == IOMode.TXT:
            out = ''.join(map(chr, out))
        return out

    def flush(self):
        self.out_queue.clear()
        if self.status != Status.HLT:
            self.status == Status.RUN

    def read_lines(self):
        if not self.iomode == IOMode.TXT:
            raise OpError('Only valid in text mode')

        while True:
            status = self.run()
            if status != Status.RDY:
                break
            line = self.read()
            yield line[:-1] # Apperantly intcode is running UNIX

    def load(self, addr):
        if addr >= len(self.memory):
            msg = f'Could not load value from invalid adress {addr}'
            raise MemoryAccessError(msg)
        return self.memory[addr]

    def store(self, addr, val):
        if addr >= len(self.memory):
            msg = f'Could not store value to invalid address {addr}'
            raise MemoryAccessError(msg)
        self.memory[addr] = val

    def load_param(self, param):
        mode = self.modes[param]
        pos = self.instr_pointer + param + 1

        if mode == 0:
            # Position mode
            addr = self.load(pos)
            val  = self.load(addr)
        elif mode == 1:
            # Immediate mode
            val = self.load(pos)
        elif mode == 2:
            # Relative mode
            offset = self.load(pos)
            addr   = self.relative_base + offset
            val    = self.load(addr)
        else:
            msg = f'Invalid load mode {mode}'
            raise OpError(msg)
        return val

    def store_param(self, param, val):
        mode = self.modes[param]
        pos = self.instr_pointer + param + 1
        if mode == 0:
            # Position mode
            addr = self.load(pos)
        elif mode == 2:
            # Relative mode
            offset = self.load(pos)
            addr = self.relative_base + offset
        else:
            msg = f'Invalid store mode {mode}'
            raise OpError(msg)
        self.store(addr, val)

    def current_instr(self):
        instr = self.load(self.instr_pointer)
        instr, opcode = divmod(instr, 100)
        instr, mode0  = divmod(instr, 10)
        instr, mode1  = divmod(instr, 10)
        _    , mode2  = divmod(instr, 10)
        return opcode, (mode0, mode1, mode2)

    def step(self):
        if self.status == Status.HLT:
            return
        self.status = Status.RUN

        opcode, self.modes = self.current_instr()
        if opcode not in self.opcodes:
            msg = f'Invalid opcode {opcode} at address {self.instr_pointer}'
            raise ExecutionError(msg)

        self.opcodes[opcode]()

    def op_add(self):
        a = self.load_param(0)
        b = self.load_param(1)
        self.store_param(2, a+b)
        self.instr_pointer += 4

    def op_mul(self):
        a = self.load_param(0)
        b = self.load_param(1)
        self.store_param(2, a*b)
        self.instr_pointer += 4

    def op_inp(self):
        if len(self.inp_queue) == 0:
            self.status = Status.WFI
            return
        val = self.inp_queue.pop()
        self.store_param(0, val)
        self.instr_pointer += 2

    def op_out(self):
        val = self.load_param(0)
        self.out_queue.appendleft(val)
        self.instr_pointer += 2
        if self.iomode == IOMode.TXT:
            if val == 10:
                self.status = Status.RDY

    def op_jit(self):
        val = self.load_param(0)
        if val != 0:
            addr = self.load_param(1)
            self.instr_pointer = addr
        else:
            self.instr_pointer += 3

    def op_jif(self):
        val = self.load_param(0)
        if val == 0:
            addr = self.load_param(1)
            self.instr_pointer = addr
        else:
            self.instr_pointer += 3

    def op_lt(self):
        a = self.load_param(0)
        b = self.load_param(1)
        self.store_param(2, int(a < b))
        self.instr_pointer += 4

    def op_eq(self):
        a = self.load_param(0)
        b = self.load_param(1)
        self.store_param(2, int(a == b))
        self.instr_pointer += 4

    def op_adj(self):
        offset = self.load_param(0)
        self.relative_base += offset
        self.instr_pointer += 2

    def op_hlt(self):
        self.status = Status.HLT
