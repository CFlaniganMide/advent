from intcode import Intcode

if __name__ == "__main__":
    with open('./input.txt') as f:
        programStr = f.read()
    computer = Intcode(programStr)
    program = computer.runToHalt(inputs=[1])
    print(program)
