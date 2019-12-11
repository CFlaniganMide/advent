import itertools

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class Line(object):
    def __init__(self, coords, length):
        self.start = coords[0:2]
        self.end = coords[2:4]
        self.length = length

    def intersects(self, other):
        # boundary checking
        if self.start == [0, 0] == other.start:
            return None
        if min(self.start[0], self.end[0]) > max(other.start[0], other.end[0]):
            return None
        if min(self.start[1], self.end[1]) > max(other.start[1], other.end[1]):
            return None
        if max(self.start[0], self.end[0]) < min(other.start[0], other.end[0]):
            return None
        if max(self.start[1], self.end[1]) < min(other.start[1], other.end[1]):
            return None

        if type(self) == type(other):
            raise TypeError("Not sure how to handle parallel lines yet")

        if isinstance(self, VertLine):
            intersection = [self.start[0], other.start[1]]
        else:
            intersection = [other.start[0], self.start[1]]

        return sum(intersection), self.length + manhattan(self.start, intersection), \
               other.length + manhattan(other.start, intersection)

class HorzLine(Line):
    def __repr__(self):
        return "<HorzLine: (%d, %d), (%d, %d)>" % (self.start[0], self.start[1], self.end[0], self.end[1])

class VertLine(Line):
    def __repr__(self):
        return "<VertLine: (%d, %d), (%d, %d)>" % (self.start[0], self.start[1], self.end[0], self.end[1])

class Wire(object):

    def __init__(self, lineStr):
        self.path = lineStr
        self.lines = []

        coord = [0, 0]
        length = 0
        for line in lineStr.split(','):
            dist = int(line[1:])
            if line[0] == "U":
                self.lines.append(VertLine([*coord, coord[0], coord[1] + dist], length))
                coord[1] += dist
            if line[0] == "D":
                self.lines.append(VertLine([*coord, coord[0], coord[1] - dist], length))
                coord[1] -= dist
            if line[0] == "L":
                self.lines.append(HorzLine([*coord, coord[0] - dist, coord[1]], length))
                coord[0] -= dist
            if line[0] == "R":
                self.lines.append(HorzLine([*coord, coord[0] + dist, coord[1]], length))
                coord[0] += dist
            length += dist

    def intersections(self, other):
        inters = []

        for lSelf in self.lines:
            for lOther in other.lines:
                lInter = lSelf.intersects(lOther)
                if lInter is not None:
                    print(lInter)
                    inters.append(lInter)

        return inters

    def intersectionsDost(self, other):
        inters = []

        for lSelf in self.lines:
            for lOther in other.lines:
                lInter = lSelf.intersects(lOther)
                if lInter is not None:
                    print(lInter)
                    inters.append(lInter)

        return inters


def run(lineStr1, lineStr2):
    line1 = Wire(lineStr1)
    line2 = Wire(lineStr2)

    intersections = line1.intersections(line2)

    return min([x[0] for x in intersections])

def runDist(lineStr1, lineStr2):
    line1 = Wire(lineStr1)
    line2 = Wire(lineStr2)

    intersections = line1.intersections(line2)

    print([x[0] for x in intersections])
    print([sum(x[1:3]) for x in intersections])

    return min([sum(x[1:3]) for x in intersections])

if __name__ == "__main__":
    with open('./input.txt') as f:
        lines = f.readlines()
        print(run(*lines))
        print(runDist(*lines))
