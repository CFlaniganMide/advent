import unittest

from . import day6


class MyTestCase(unittest.TestCase):
    def test_day6_1(self):
        testInput = ["COM)B",
                     "B)C",
                     "C)D",
                     "D)E",
                     "E)F",
                     "B)G",
                     "G)H",
                     "D)I",
                     "E)J",
                     "J)K",
                     "K)L"]
        bodies = day6.buildOrbitalTree(testInput)
        self.assertEqual(day6.hyperDescendants(bodies), 42)

    def test_day6_2(self):
        testInput = ["COM)B",
                     "B)C",
                     "C)D",
                     "D)E",
                     "E)F",
                     "B)G",
                     "G)H",
                     "D)I",
                     "E)J",
                     "J)K",
                     "K)L",
                     "K)YOU",
                     "I)SAN"]
        bodies = day6.buildOrbitalTree(testInput)
        self.assertEqual(bodies['YOU'].distance(bodies['SAN']) - 2, 4)


if __name__ == '__main__':
    unittest.main()
