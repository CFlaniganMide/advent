import unittest

import numpy as np

from . import day10



class MyTestCase(unittest.TestCase):
    def test_day10_0(self):
        input = [".#..#",
                 ".....",
                 "#####",
                 "....#",
                 "...##"]
        astroMap = day10.AstroGraph(input)
        print(astroMap.drawMap())
        np.testing.assert_array_equal(astroMap.drawMap(), np.array([[".", "7", ".", ".", "7"],
                                                             [".", ".", ".", ".", "."],
                                                             ["6", "7", "7", "7", "5"],
                                                             [".", ".", ".", ".", "7"],
                                                             [".", ".", ".", "8", "7"]]))
        self.assertEqual(astroMap.maxEdges, (8, [3, 4]))

    def test_day10_1(self):
        input = ["......#.#.",
                 "#..#.#....",
                 "..#######.",
                 ".#.#.###..",
                 ". ..#.....",
                 "..#....#.#",
                 "#..#....#.",
                 ".##.#..###",
                 "##...#..#.",
                 ".#....####"]
        astroMap = day10.AstroGraph(input)
        print(astroMap.drawMap())
        print(astroMap.maxEdges)
        self.assertEqual(astroMap.maxEdges, (33, [5, 8]))

    def test_day10_2(self):
        input = ["#.#...#.#.",
                 ".###....#.",
                 ".#....#...",
                 "##.#.#.#.#",
                 "....#.#.#.",
                 ".##..###.#",
                 "..#...##..",
                 "..##....##",
                 "......#...",
                 ".####.###."]
        astroMap = day10.AstroGraph(input)
        print(astroMap.drawMap())
        print(astroMap.maxEdges)
        self.assertEqual(astroMap.maxEdges, (35, [1, 2]))




if __name__ == '__main__':
    unittest.main()
