import itertools
import math

import numpy as np

def genCoords(inputLines):
    starMap = np.ones((len(inputLines[0]), len(inputLines)), dtype=object)
    for y, line in enumerate(inputLines):
        for x, cell in enumerate(line):
            starMap[x, y] = cell
    return starMap


def dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


class Node(object):
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.edges = []
        self.coords = coords

    def makeLine(self, other):

        if abs(self.x - other.x) == 1 or abs(self.y - other.y) == 1:
            # otherwise, if one coordinate is different by one, it's still super easy (always true)
            return []
        # flat lines are easy
        if self.x == other.x:
            return [[self.x, y] for y in range(min(self.y, other.y) + 1, max(self.y, other.y))]
        elif self.y == other.y:
            return [[x, self.y] for x in range(min(self.x, other.x) + 1, max(self.x, other.x))]
        else:

            gcd = math.gcd(self.x - other.x, self.y - other.y)
            if gcd == 1:
                return []
            step = ((other.x - self.x) / gcd, (other.y - self.y) / gcd)
            return [[self.x + i*step[0], self.y + i*step[1]] for i in range(1, gcd)]

    def __repr__(self):
        return "<Node: [%s, %s]>" % tuple(self.coords)

class AstroGraph(object):
    def __init__(self, inputLines):
        self.width = len(inputLines[0])
        self.height = len(inputLines)

        self._lines = []

        # Generate a list of coordinates from the input lines
        coords = genCoords(inputLines)

        # Convert coordinates into graph nodes
        self.nodes = [Node([x, y]) for x, y in zip(*np.where(coords == "#"))]
        for nodeA, nodeB in itertools.combinations(self.nodes, 2):
            self.checkLoS(nodeA, nodeB)

    def checkLoS(self, nodeA, nodeB):
        line = nodeA.makeLine(nodeB)
        if len(line) > 0:
            for node in self.nodes:
                # If a node is on the line between the nodes,
                # and the node is neither of the endpoints,
                # return without adding edges
                if node.coords in line:
                    return
        nodeA.edges.append(nodeB)
        nodeB.edges.append(nodeA)

    def drawMap(self):
        map = np.full((self.height, self.width), ".", dtype=object)
        for n in self.nodes:
            map[n.y, n.x] = str(len(n.edges))
        return map

    @property
    def maxEdges(self):
        return max([(len(n.edges), n.coords) for n in self.nodes], key=lambda x: x[0])

    @property
    def maxNode(self):
        return max([n for n in self.nodes], key=lambda x: len(x.edges))


if __name__ == "__main__":
    with open("./input.txt") as f:
        inputLines = f.readlines()
    aMap = AstroGraph(inputLines)
    print(aMap.maxEdges)

    maxNode = aMap.maxNode

    # sort asteroids with edges to the maximum, by angle from upwards (atan2 rotated 90 degrees ccw)
    print(sorted(maxNode.edges, key=lambda n: math.atan2(n.y - maxNode.y, maxNode.x - n.x))[200])
