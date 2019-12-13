
class Body(object):
    def __init__(self, id):
        self.id = id
        self.children = []
        self.parent = None

    def __repr__(self):
        return "<Body ID:%s>" % (self.id,)

    @property
    def suborbits(self):
        return len(self.children) + sum([x.suborbits for x in self.children])

    def recEdges(self):
        return self.suborbits + sum([x.recEdges() for x in self.children])

    def isDescendant(self, target):
        if target in self.children:
            return True
        for child in self.children:
            if child.isDescendant(target):
                return True
        return False

    def distance(self, target):
        if self.isDescendant(target):
            if target in self.children:
                return 1
            else:
                for child in self.children:
                    if child.isDescendant(target):
                        return 1 + child.distance(target)
        else:
            return 1 + self.parent.distance(target)

def buildOrbitalTree(inputs):

    bodies = {}

    orbits = [x.split(')') for x in inputs]

    for parentStr, childStr in orbits:
        if parentStr in bodies.keys():
            parent = bodies[parentStr]
        else:
            parent = Body(parentStr)
            bodies[parentStr] = parent

        if childStr in bodies.keys():
            child = bodies[childStr]
        else:
            child = Body(childStr)
            bodies[childStr] = child

        child.parent = parent
        parent.children.append(child)
    return bodies

def hyperDescendants(tree):
    return sum([x.recEdges() for x in tree.values() if x.parent is None])


if __name__ == "__main__":
    with open('./input.txt') as f:
        inputs = f.readlines()
    inputs = [x.strip('\n') for x in inputs]
    bodies = buildOrbitalTree(inputs)

    print(hyperDescendants(bodies))

    you = bodies['YOU']
    san = bodies['SAN']

    print(you.distance(san) - 2)


