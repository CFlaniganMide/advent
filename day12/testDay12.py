import unittest

from .day12 import *


class TestDay12(unittest.TestCase):

    def test_day_12_0(self):
        inputLines = ["<x=-1, y=0, z=2>",
                      "<x=2, y=-10, z=-7>",
                      "<x=4, y=-8, z=8>",
                      "<x=3, y=5, z=-1>"]
        bodies = []
        coordPattern = re.compile("<x=(.+), y=(.+), z=(.+)>")
        for line in inputLines:
            bodies.append(Body([int(x) for x in coordPattern.findall(line)[0]]))
        sim = Simulation(bodies)
        sim.step(10)
        self.assertEqual(179, sim.energy)

    def test_day_12_1(self):
        inputLines = ["<x=-1, y=0, z=2>",
                      "<x=2, y=-10, z=-7>",
                      "<x=4, y=-8, z=8>",
                      "<x=3, y=5, z=-1>"]
        bodies = []
        coordPattern = re.compile("<x=(.+), y=(.+), z=(.+)>")
        for line in inputLines:
            bodies.append(Body([int(x) for x in coordPattern.findall(line)[0]]))
        sim = Simulation(bodies)
        simArray = np.stack([np.append(x.position, x.velocity) for x in sim.bodies])
        steps = compiledSim(simArray)
        self.assertEqual(2772, steps)

    def test_day_12_2(self):
        inputLines = ["<x=-8, y=-10, z=0>",
                      "<x=5, y=5, z=10>",
                      "<x=2, y=-7, z=3>",
                      "<x=9, y=-8, z=-3>"]

        bodies = []
        coordPattern = re.compile("<x=(.+), y=(.+), z=(.+)>")
        for line in inputLines:
            bodies.append(Body([int(x) for x in coordPattern.findall(line)[0]]))
        sim = Simulation(bodies)
        simArray = np.stack([np.append(x.position, x.velocity) for x in sim.bodies])
        steps = compiledSim(simArray)
        self.assertEqual(4686774924, steps)


if __name__ == '__main__':
    unittest.main()
