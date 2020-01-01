import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np

from intcode import Intcode


class Cabinet:

    def __init__(self, programStr):
        self.programStr = programStr
        self.computer = Intcode(programStr)
        self.program = self.computer.run()
        self.screen = np.zeros((50, 50))
        self.segDisp = 0
        self._x = 0
        self._y = 0


    def printChars(self):
        while not self.computer.halted:
            try:
                x = next(self.program)
                y = next(self.program)
                val = next(self.program)
                if x is None or y is None or val is None:
                    return

                if x == -1 and y == 0:
                    self.segDisp = val
                else:
                    self._x = max(x + 1, self._x)
                    self._y = max(y + 1, self._y)
                    self.screen[x, y] = val
            except Exception as e:
                print(e)
                if not isinstance(e, StopIteration):
                    raise e
                else:
                    self.screen = self.screen[:self._x, :self._y]
                    return

    def reset(self):
        # self.screen = np.zeros_like(self.screen)
        self.computer.run(inputs=[0], reset=True)

    def play(self):
        # loop forever
        # f = plt.figure()
        while np.sum(self.screen == 2) > 0:
            pass
            # Print and display the screen
            self.printChars()
            # plt.pcolormesh(cab.screen[:, ::-1].T, cmap="tab10")
            # plt.show()

            # update intcode computer
            (px,), (py,) = np.where(self.screen == 3)
            (bx,), (by,) = np.where(self.screen == 4)
            if bx == px:
                move = 0
            elif bx < px:
                move = -1
            else:
                move = 1

            """

            # get user input
            inChar = input()
            if inChar == "a":
                move = -1
            elif inChar == "s":
                move = 0
            elif inChar == "d":
                move = 1
            else:
                move = 0
            """

            # run intcode computer
            self.program = self.computer.run(inputs=[move], reset=False)



if __name__ == "__main__":
    with open("input.txt") as f:
        programStr = f.read()
    cab = Cabinet(programStr)
    cab.printChars()

    plt.pcolormesh(cab.screen[:, ::-1].T, cmap="tab10")
    plt.show()
    print(np.sum(cab.screen == 2))

    cab.reset()
    cab.computer.program[0] = 2
    cab.printChars()
    plt.pcolormesh(cab.screen[:, ::-1].T, cmap="tab10")
    plt.show()
    cab.play()

    print(cab.segDisp)
