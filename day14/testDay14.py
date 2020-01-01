import unittest

from .day14 import *


class TestDay14(unittest.TestCase):
    def test_day14_0(self):
        with open('./day14/testInput1.txt') as f:
            reactionStrs = f.readlines()
        refinery = Refinery(reactionStrs)
        refinery.fuel.add(1)
        self.assertEqual(13312, refinery['ORE'].total)

    def test_day14_1(self):
        with open('./day14/testInput2.txt') as f:
            reactionStrs = f.readlines()
        refinery = Refinery(reactionStrs)
        refinery.fuel.add(1)
        self.assertEqual(180697, refinery['ORE'].total)

    def test_day14_2(self):
        with open('./day14/testInput3.txt') as f:
            reactionStrs = f.readlines()
        refinery = Refinery(reactionStrs)
        refinery.fuel.add(1)
        self.assertEqual(2210736, refinery['ORE'].total)

    def test_day14_3(self):
        with open('./day14/testInput1.txt') as f:
            reactionStrs = f.readlines()
        refinery = Refinery(reactionStrs)
        self.assertEqual(82892753, int(Fraction(int(1e12), 1)/refinery.fuel.oreRatio()))

    def test_day14_4(self):
        with open('./day14/testInput2.txt') as f:
            reactionStrs = f.readlines()
        refinery = Refinery(reactionStrs)
        self.assertEqual(5586022, int(Fraction(int(1e12), 1)/refinery.fuel.oreRatio()))

    def test_day14_5(self):
        with open('./day14/testInput3.txt') as f:
            reactionStrs = f.readlines()
        refinery = Refinery(reactionStrs)
        self.assertEqual(460664, int(Fraction(int(1e12), 1)/refinery.fuel.oreRatio()))


if __name__ == '__main__':
    unittest.main()
