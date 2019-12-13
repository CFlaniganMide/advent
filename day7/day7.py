from intcode import Intcode

from itertools import permutations

def maxAmplifiers(programStr):

    computer = Intcode(programStr)

    outputList = []

    for phases in permutations(range(5), 5):
        inputs = [0]
        for i, p in enumerate(phases):
            inputs += computer.runToHalt([p, inputs[i]])

        outputList.append(inputs[-1])
    return max(outputList)

def maxerAmplifiers(programStr):

    computers = [Intcode(programStr) for _ in range(5)]

    outputList = []

    for phases in permutations(range(5, 10), 5):
        programs = [(c, c.run(inputs=[p])) for c, p in zip(computers, phases)]

        thisInput = 0
        while True:
            c, p = programs.pop(0)
            c.inputs.append(thisInput)
            nextInput = next(p, None)
            if nextInput is None:
                break
            thisInput = nextInput
            programs.append((c, p))
        outputList.append(thisInput)
    return max(outputList)


if __name__ == "__main__":
    with open('./input.txt') as f:
        programStr = f.read()
        print(maxAmplifiers(programStr))
        print(maxerAmplifiers(programStr))

