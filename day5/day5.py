def getAddr(program, idx, nArgs):
    addrs = []

    instruction = program[idx]//100

    for i in range(0, nArgs):
        mode = instruction % 10
        instruction //= 10
        if mode == 0:
            addrs.append(program[idx+1+i])
        else:
            addrs.append(idx+1+i)

    return tuple(addrs)


def run(program, inputs=None):
    idx = 0
    while program[idx] != 99:

        instruction = program[idx]
        opcode = instruction % 100

        if opcode == 1:
            (addr1, addr2) = getAddr(program, idx, 2)
            program[program[idx+3]] = program[addr1] + program[addr2]
            idx += 4
        elif opcode == 2:
            (addr1, addr2) = getAddr(program, idx, 2)
            program[program[idx+3]] = program[addr1] * program[addr2]
            idx += 4
        elif opcode == 3:
            program[program[idx+1]] = inputs.pop(0)
            idx += 2
        elif opcode == 4:
            (addr1,) = getAddr(program, idx, 1)
            print(idx, program[addr1])
            idx += 2
        elif opcode == 5:
            (addr1, addr2) = getAddr(program, idx, 2)
            if program[addr1] != 0:
                idx = program[addr2]
            else:
                idx += 3
        elif opcode == 6:
            (addr1, addr2) = getAddr(program, idx, 2)
            if program[addr1] == 0:
                idx = program[addr2]
            else:
                idx += 3
        elif opcode == 7:
            (addr1, addr2) = getAddr(program, idx, 2)
            program[program[idx + 3]] = int(program[addr1] < program[addr2])
            idx += 4
        elif opcode == 8:
            (addr1, addr2) = getAddr(program, idx, 2)
            program[program[idx + 3]] = int(program[addr1] == program[addr2])
            idx += 4
        else:
            raise Exception()
    return program[0]

if __name__ == "__main__":
    with open('./input.txt') as f:
        programStr = f.read()

    program = [int(x) for x in programStr.split(',')]
    print(run(program, [1]))

    program = [int(x) for x in programStr.split(',')]
    print(run(program, [5]))


