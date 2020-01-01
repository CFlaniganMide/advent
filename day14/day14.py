from fractions import Fraction
import math

from tqdm import tqdm
import numba as nb


class Reaction:
    def __init__(self, string, parent):
        string = string.strip("\r\n")
        inputStr, outputStr = string.split(" => ")

        self.reagents = [[int(x), y] for x, y in [z.split(" ") for z in inputStr.split(", ")]]

        self.yieldNum, self.id = outputStr.split(" ")
        self.yieldNum = int(self.yieldNum)

        self.parent = parent

    def __repr__(self):
        try:
            return "<Reaction: %s <= %s>" % (self.id, ", ".join(["%d %s" % (x[0], x[1].id) for x in self.reagents]))
        except Exception as e:
            return str(e)

    def update(self):
        for i, reagent in enumerate(self.reagents):
            self.reagents[i][1] = self.parent[reagent[1]]


    def add(self, num):
        # the number of reactions is the target yield divided by the yield ratio, rounded up
        nReacts = math.ceil(num/self.yieldNum)

        # for every component
        for rNum, reagent in self.reagents:

            # the required number reagents for this reaction is the number of reactions times the number of reagents
            # reaction
            required = nReacts*rNum

            # if there are fewer of the reagent than needed,
            if required > self.parent.components[reagent.id]:
                # add the difference to the required reagent
                reagent.add(required - self.parent.components[reagent.id])

            # subtract the required amount of the reagent
            self.parent.components[reagent.id] -= required

        # add yield to the available components
        self.parent.components[self.id] += self.yieldNum*nReacts

    def oreRatio(self):

        ratio = 0  # Fraction(0, 1)

        # add the cost of reach reagent for this reaction
        for rNum, reagent in self.reagents:
            ratio += float(Fraction(rNum, self.yieldNum)) * reagent.oreRatio()

        return float(ratio)



class Refinery:
    def __init__(self, reactionStrs):
        self.reactions = [Reaction(s, self) for s in reactionStrs]
        self.fuel = next(x for x in self.reactions if x.id == 'FUEL')
        self.reactions.append(Ore(self))
        self.components = {x.id: 0 for x in self.reactions}

        [x.update() for x in self.reactions]

    def __getitem__(self, item):
        for reaction in self.reactions:
            if reaction.id == item:
                return reaction

    def reset(self):
        for c in self.components.keys():
            self.components[c] = 0
        self['ORE'].total = 0


class Ore(Reaction):
    def __init__(self, parent):
        self.id = "ORE"
        self.parent = parent
        self.total = 0

    def __repr__(self):
        return "<Reaction: ORE>"

    def update(self):
        pass

    def add(self, num):
        self.total += num
        self.parent.components[self.id] = num

    def oreRatio(self):
        return float(Fraction(1, 1))


if __name__ == "__main__":
    with open('input.txt') as f:
        reactionStrs = f.readlines()
    refinery = Refinery(reactionStrs)
    refinery.fuel.add(1)

    print(refinery['ORE'].total)

    refinery.reset()
    refinery.fuel.add(1e12)

    print(float(Fraction(int(1e12), 1)/refinery.fuel.oreRatio()))
    print(refinery['ORE'].total)

    firstGuess = refinery['ORE'].total

    target = 1e12

    maxBound = 1e3

    refinery.reset()
    refinery.fuel.add(maxBound)

    val = refinery['ORE'].total

    while val < target:
        maxBound *= 2
        refinery.reset()
        refinery.fuel.add(maxBound)
        val = refinery['ORE'].total

    minBound = maxBound / 2

    pivot = int((minBound + maxBound)/2)

    refinery.reset()
    refinery.fuel.add(pivot)


    while True:
        val = refinery['ORE'].total
        print(val/target)

        if val > target:
            maxBound = pivot
        elif val < target:
            minBound = pivot
        else:
            break

        if maxBound - minBound == 1:
            break

        pivot = int((minBound + maxBound)/2)

        refinery.reset()
        refinery.fuel.add(pivot)

    print(pivot)
