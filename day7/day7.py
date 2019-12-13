from intcode import Intcode

from itertools import permutations

def maxAmplifiers(programStr):

    computer = Intcode(programStr)

    outputList = []

    for phases in permutations(range(5), 5):
        inputs = [0]
        for i, p in enumerate(phases):
            inputs += computer.run([p, inputs[i]])\

        outputList.append(inputs[-1])
    return max(outputList)

def maxerAmplifiers(programStr):

    computers = [Intcode(programStr) for _ in range(5)]

    outputList = []

    for phases in permutations(range(5, 10), 5):
        for c in computers:
            c.updateProgram()
        inputs = [0]

        firstRun = True
        while not computers[0].halted:
            for i, p in enumerate(phases):
                thisInput = inputs[-1]
                if firstRun:
                    nextInput = computers[i].run(inputs=[p, thisInput], reset=False, returnOnOut=True)
                else:
                    nextInput = computers[i].run(inputs=[thisInput], reset=False, returnOnOut=True)

                if nextInput is not None:
                    inputs.append(nextInput)
                else:
                    break

            firstRun = False
        outputList.append(inputs[-1])
    return max(outputList)


if __name__ == "__main__":
    with open('./input.txt') as f:
        programStr = f.read()
        print(maxAmplifiers(programStr))
        print(maxerAmplifiers(programStr))

