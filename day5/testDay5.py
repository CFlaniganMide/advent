import unittest

from . import day5


class MyTestCase(unittest.TestCase):
    def test_day2(self):
        programStr = "1,9,10,3,2,3,11,0,99,30,40,50"
        program = [int(x) for x in programStr.split(',')]
        self.assertEqual(day5.run(program), 3500)

    def test_day5(self):
        programStr = "3,0,4,0,99"
        program = [int(x) for x in programStr.split(',')]
        self.assertEqual(day5.run(program, [1]), 1)


if __name__ == '__main__':
    unittest.main()
