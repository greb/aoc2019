import enum

class ExecutionError(Exception):
    pass

class MemoryAccessError(Exception):
    pass

class Status(enum.Enum):
    RUN = 'run'
    HLT = 'halt'

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
    def __init__(self, code):
        self.rom = parse_code(code)
        self.reset()
        self.opcodes = {
            1: self.op_add,
            2: self.op_mul,
            99: self.op_hlt
        }

    def reset(self):
        self.memory = self.rom.copy()
        self.instr_pointer = 0
        self.status = Status.RUN

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
        addr = self.load(self.instr_pointer + param)
        return self.load(addr)

    def store_param(self, param, val):
        addr = self.load(self.instr_pointer + param)
        self.store(addr, val)

    def current_instr(self):
        return self.load(self.instr_pointer)

    def step(self):
        if self.status == Status.HLT:
            return self.status

        opcode = self.current_instr()
        if opcode not in self.opcodes:
            msg = f'Invalid opcode {opcode} at address {self.instr_pointer}'
            raise ExecutionError(msg)

        self.opcodes[opcode]()

    def run(self):
        while self.status == Status.RUN:
            self.step()
        return self.status

    def op_add(self):
        a = self.load_param(1)
        b = self.load_param(2)
        self.store_param(3, a+b)
        self.instr_pointer += 4

    def op_mul(self):
        a = self.load_param(1)
        b = self.load_param(2)
        self.store_param(3, a*b)
        self.instr_pointer += 4

    def op_hlt(self):
        self.status = Status.HLT
