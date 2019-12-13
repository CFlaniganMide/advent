import unittest

from . import day7


class TestDay7(unittest.TestCase):
    def test_day7_0(self):
        programStr = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"

        self.assertEqual(day7.maxAmplifiers(programStr), 43210)

    def test_day7_1(self):
        programStr = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"

        self.assertEqual(day7.maxerAmplifiers(programStr), 139629729)


if __name__ == '__main__':
    unittest.main()
