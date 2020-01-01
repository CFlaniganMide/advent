import numpy as np
import matplotlib.pyplot as plt

from intcode import Intcode


class Robot:
    def __init__(self, programStr):
        self.computer = Intcode(programStr)
        self.program = self.computer.run()
        self.direction = "^"
        self.x = 100
        self.y = 100
        self.world = np.zeros((200, 200))
        self.modifiedSpaces = []

    @property
    def pos(self):
        return self.x, self.y

    def move(self):
        self.computer.inputs.append(self.world[self.x, self.y])

        oldColor = self.world[self.x, self.y]

        self.world[self.x, self.y] = next(self.program)
        if oldColor != self.world[self.x, self.y]:
            self.modifiedSpaces.append(self.pos)

        dir = next(self.program)

        if dir == 0:
            self.turnLeft()
        elif dir == 1:
            self.turnRight()
        else:
            raise ValueError()

        if self.direction == "^":
            self.y += 1
        elif self.direction == "<":
            self.x -= 1
        elif self.direction == "v":
            self.y -= 1
        elif self.direction == ">":
            self.x += 1
        else:
            raise ValueError()

    def turnLeft(self):
        if self.direction == "^":
            self.direction = "<"
        elif self.direction == "<":
            self.direction = "v"
        elif self.direction == "v":
            self.direction = ">"
        elif self.direction == ">":
            self.direction = "^"
        else:
            raise ValueError()

    def turnRight(self):
        if self.direction == "^":
            self.direction = ">"
        elif self.direction == "<":
            self.direction = "^"
        elif self.direction == "v":
            self.direction = "<"
        elif self.direction == ">":
            self.direction = "v"
        else:
            raise ValueError()


if __name__ == "__main__":
    with open('./input.txt') as f:
        programStr = f.read()
    robot = Robot(programStr)
    running = True
    while running:
        try:
            robot.move()
        except Exception as e:
            print(e)
            running = False
    plt.pcolormesh(robot.world)
    plt.show()

    print(len(set(robot.modifiedSpaces)))

    robot2 = Robot(programStr)
    robot2.world[robot2.x, robot2.y] = 1
    running = True
    while running:
        try:
            robot2.move()
        except Exception as e:
            print(e)
            running = False
    plt.pcolormesh(robot2.world)
    plt.show()

    print(len(set(robot2.modifiedSpaces)))



