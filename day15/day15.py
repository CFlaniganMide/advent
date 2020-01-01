import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

from intcode import Intcode

UNEXPLORED = 0
WALL = 1
CLEAR = 2
TARGET = 3


def manhattan(position, target):
    diff = np.abs(target - np.expand_dims(position, 1))
    return (diff[0, :] + diff[1, :]).min()


class Robot:
    """ Robot explorer agent.  Does his best.  Has methods for exploring and navigating this crazy world we call home.
    """
    def __init__(self, programStr, worldSize=50):
        self.programStr = programStr
        self.computer = Intcode(self.programStr)
        self.program = self.computer.run()
        self.program.send(None)
        self.world = Map(worldSize, worldSize)
        self.position = np.array((0, 0))

    def reset(self):
        self.computer = Intcode(self.programStr)
        self.program = self.computer.run()
        self.program.send(None)
        self.position = np.array((0, 0))
        self.world.reset()

    def move(self, direction):
        if direction == "north" or direction == 1:
            cmd = 1
            move = np.array((0, 1))
        elif direction == "south" or direction == 2:
            cmd = 2
            move = np.array((0, -1))
        elif direction == "west" or direction == 3:
            cmd = 3
            move = np.array((-1, 0))
        elif direction == "east" or direction == 4:
            cmd = 4
            move = np.array((1, 0))
        else:
            raise ValueError()

        self.computer.inputs.append(cmd)
        response = next(self.program)

        if response == 0:
            self.world.setWall(self.position + move)
            move = np.array((0, 0))
        elif response == 1:
            self.world.setClear(self.position + move)
        elif response == 2:
            self.world.setTarget(self.position + move)
        else:
            raise ValueError()

        self.position += move

        return response

    def explore(self):
        """ Frontier expansion algorithm.  I like the navy paper, personally.  It's a bit overkill, and it doesn't quite
            fit, but I'm going to use it as a base.  While there exists an active frontier, navigate to the nearest
            frontier.  No grouping, since I don't have a lidar unit.  Implementation will be an A* algorithm where the
            heuristic is the minimum of the manhattan distance to the frontiers.
            Distance = manhattan
            frontier = any unexplored node adjacent to a clear or target node
            active frontier = any frontier which can be navigated to from the current position
        """
        while self.world.hasFrontier():
            direction = self.navigate(self.world.frontiers())
            self.move(direction)

    def navigate(self, target, mode="direction"):
        """ A* navigate, from current position to target.  if target is a scalar, use the appropriate code to find where
            that is.  If it's a length 2 array, then it's a single target, if it's a 2xn array then it's a list of valid
            targets
        """
        self.world.gScoreReset()

        # a list of paths on the frontier (yes, this is confusing)
        # each path has a g score (path length) and an h score (heuristic score)
        openSet = [self.position]
        self.world.setG(self.position, 0)
        self.world.setH(self.position, manhattan(self.position, target))

        cameFrom = {}

        while len(openSet) > 0:
            # sort the open set by f score
            openSet = sorted(openSet, key=lambda x: self.world.getF(x))
            current = openSet.pop(0)

            # current is in target
            if np.any(np.all(target == np.expand_dims(current, 1), axis=0)):
                path = []
                while np.any(current != tuple(self.position)):
                    path.append(current)
                    current = np.array(cameFrom[tuple(current)])
                path.append(current)

                if mode == "direction":
                    direction = path[-2] - path[-1]
                    if direction[0] == 0:
                        if direction[1] == 1:
                            return "north"
                        else:
                            return "south"
                    elif direction[0] == 1:
                        return "east"
                    else:
                        return "west"
                elif mode == "path":
                    return path
                else:
                    raise ValueError()

            # otherwise,
            for move in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                move = np.array(move)
                if not self.world.valid(current + move):
                    continue
                if self.world.getH(current + move) == 99999:
                    self.world.setH(current + move, manhattan(current + move, target))

                tentativeG = self.world.getG(current) + 1
                if tentativeG < self.world.getG(current + move):
                    cameFrom[tuple(current + move)] = tuple(current)
                    self.world.setG(current + move, tentativeG)
                    if tuple(current + move) not in [tuple(x) for x in openSet]:
                        openSet.append(current + move)



class Map:
    """ Map for the whole dealio.  Uses an offset so agents can start in the middle and also be at (0, 0).
    """
    def __init__(self, width, height):
        self.offset = np.array((width//2, height//2))
        self.body = np.zeros((width, height))
        self.gScore = np.ones_like(self.body)*99999
        self.hScore = np.ones_like(self.body)*99999

    def reset(self):
        self.body = np.zeros_like(self.body)
        self.gScore = np.ones_like(self.body)*99999
        self.hScore = np.ones_like(self.body)*99999

    def setWall(self, coord):
        self.body[tuple(coord + self.offset)] = WALL

    def setClear(self, coord):
        self.body[tuple(coord + self.offset)] = CLEAR

    def setTarget(self, coord):
        self.body[tuple(coord + self.offset)] = TARGET

    def hasFrontier(self):
        adjacentKernel = np.array([[0, 1, 0],
                                   [1, 0, 1],
                                   [0, 1, 0]])
        clear = sig.convolve2d((self.body == CLEAR) + (self.body == TARGET), adjacentKernel, mode='same') > 0
        unexplored = self.body == UNEXPLORED
        return np.any(clear*unexplored)

    def frontiers(self):
        adjacentKernel = np.array([[0, 1, 0],
                                   [1, 0, 1],
                                   [0, 1, 0]])
        clear = sig.convolve2d((self.body == CLEAR) + (self.body == TARGET), adjacentKernel, mode='same') > 0
        unexplored = self.body == UNEXPLORED
        x, y = np.where(clear*unexplored)
        return np.stack([x - self.offset[0], y - self.offset[1]])

    def gScoreReset(self):
        self.gScore = np.ones_like(self.gScore)*99999

    def setG(self, coord, score):
        self.gScore[tuple(coord + self.offset)] = score

    def setH(self, coord, score):
        self.hScore[tuple(coord + self.offset)] = score

    @property
    def fScore(self):
        return self.gScore + self.hScore

    def getF(self, coord):
        return self.fScore[tuple(coord + self.offset)]

    def getG(self, coord):
        return self.gScore[tuple(coord + self.offset)]

    def getH(self, coord):
        return self.hScore[tuple(coord + self.offset)]

    def valid(self, coord):
        return self.body[tuple(coord + self.offset)] != WALL

    def getTarget(self, target):
        return np.stack(np.where(self.body == target)) - np.expand_dims(self.offset, 1)

    def floodFillSteps(self):
        i = 0
        validTiles = (self.body == CLEAR) + (self.body == TARGET)
        gas = self.body == TARGET
        adjacentKernel = np.array([[0, 1, 0],
                                   [1, 1, 1],
                                   [0, 1, 0]])
        while np.sum(validTiles*1 - gas*1) > 0:
            i += 1
            gas = (sig.convolve2d(gas, adjacentKernel, mode='same')*validTiles) > 0

        return i




class Path:
    def __init__(self, path, h):
        self.path = path
        self.g = len(path) - 1
        self.h = h

    def __repr__(self):
        return "<Path: (%d, %d) f:%d>" % (self.position[0], self.position[1], self.f)

    @property
    def f(self):
        return self.h + self.g

    @property
    def position(self):
        return self.path[-1]


if __name__ == "__main__":
    with open("./input.txt") as f:
        programString = f.read()
    rob = Robot(programString)
    rob.world.setClear(np.array((0, 0)))
    rob.explore()
    rob.position = np.array((0, 0))
    targetCoord = rob.world.getTarget(TARGET)
    path = rob.navigate(np.stack(targetCoord), mode="path")
    print(path)
    print(len(path) - 1)

    print(rob.world.floodFillSteps())
