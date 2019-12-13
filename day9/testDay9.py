import unittest
import math

from . import day9
from intcode import Intcode

class MyTestCase(unittest.TestCase):
    def test_day9_0(self):
        programStr = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
        computer = Intcode(programStr)
        output = computer.runToHalt()
        self.assertListEqual(output, [int(x) for x in programStr.split(',')])

    def test_day9_1(self):
        programStr = "1102, 34915192, 34915192, 7, 4, 7, 99, 0"
        computer = Intcode(programStr)
        output = computer.runToHalt()
        self.assertGreaterEqual(math.log10(output[0]), 15)

    def test_day9_2(self):
        programStr = "104,1125899906842624,99"
        computer = Intcode(programStr)
        output = computer.runToHalt()
        self.assertGreaterEqual(output[0], 1125899906842624)


if __name__ == '__main__':
    unittest.main()
