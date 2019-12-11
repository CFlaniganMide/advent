import unittest

from . import day3


class MyTestCase(unittest.TestCase):
    def test_something(self):
        testInput = ["R8,U5,L5,D3", "U7,R6,D4,L4"]

        out = day3.run(*testInput)
        self.assertEqual(out, 6)

        out = day3.runDist(*testInput)
        self.assertEqual(out, 30)


if __name__ == '__main__':
    unittest.main()
