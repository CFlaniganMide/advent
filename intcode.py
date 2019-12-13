class Intcode(object):

    program = []
    idx = 0
    halted = False
    inputs = []

    def __init__(self, programStr):
        self.programStr = programStr
        self.updateProgram()

    def updateProgram(self):
        self.program = program = [int(x) for x in self.programStr.split(',')]
        self.idx = 0
        self.halted = False

    def getAddr(self, idx, nArgs):
        addrs = []

        instruction = self.program[idx]//100

        for i in range(0, nArgs):
            mode = instruction % 10
            instruction //= 10
            if mode == 0:
                addrs.append(self.program[idx+1+i])
            else:
                addrs.append(idx+1+i)

        return tuple(addrs)


    def _requestInput(self):
        if len(self.inputs) > 0:
            return [self.inputs.pop(0)]
        else:
            yield


    def _run(self):
        while self.program[self.idx] != 99:

            instruction = self.program[self.idx]
            opcode = instruction % 100

            if opcode == 1:
                (addr1, addr2) = self.getAddr(self.idx, 2)
                addr3 = self.program[self.idx+3]
                self.program[addr3] = self.program[addr1] + self.program[addr2]
                self.idx += 4
            elif opcode == 2:
                (addr1, addr2) = self.getAddr(self.idx, 2)
                addr3 = self.program[self.idx+3]
                self.program[addr3] = self.program[addr1] * self.program[addr2]
                self.idx += 4
            elif opcode == 3:
                (addr1,) = self.getAddr(self.idx, 1)
                if len(self.inputs) > 0:
                    self.program[addr1] = self.inputs.pop(0)
                else:
                    yield
                self.idx += 2
            elif opcode == 4:
                (addr1,) = self.getAddr(self.idx, 1)
                self.idx += 2

                yield self.program[addr1]
            elif opcode == 5:
                (addr1, addr2) = self.getAddr(self.idx, 2)
                if self.program[addr1] != 0:
                    self.idx = self.program[addr2]
                else:
                    self.idx += 3
            elif opcode == 6:
                (addr1, addr2) = self.getAddr(self.idx, 2)
                if self.program[addr1] == 0:
                    self.idx = self.program[addr2]
                else:
                    self.idx += 3
            elif opcode == 7:
                (addr1, addr2) = self.getAddr(self.idx, 2)
                addr3 = self.program[self.idx+3]
                self.program[addr3] = int(self.program[addr1] < self.program[addr2])
                self.idx += 4
            elif opcode == 8:
                (addr1, addr2) = self.getAddr(self.idx, 2)
                addr3 = self.program[self.idx+3]
                self.program[addr3] = int(self.program[addr1] == self.program[addr2])
                self.idx += 4
            else:
                raise Exception()
        self.halted = True
        return

    def runToHalt(self, inputs=None, reset=True):
        if reset:
            self.updateProgram()
        self.inputs = inputs
        return list(self._run())



    def run(self, inputs=None, reset=True):
        if reset:
            self.updateProgram()
        if inputs is None:
            self.inputs = []
        else:
            self.inputs = inputs

        return self._run()

