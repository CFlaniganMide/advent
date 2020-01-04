import unittest

from .day16 import *


class TestDay16(unittest.TestCase):

    def test_filter_0(self):
        np.testing.assert_array_equal(makeFilter(0, 8), np.array([1,  0, -1,  0,  1,  0, -1,  0]))

    def test_filter_1(self):
        np.testing.assert_array_equal(makeFilter(1, 8), np.array([0,  1,  1,  0,  0, -1, -1,  0]))

    def test_filter_2(self):
        np.testing.assert_array_equal(makeFilter(2, 8), np.array([0,  0,  1,  1,  1,  0,  0,  0]))

    def test_day16_0(self):
        self.assertEqual(fft("12345678", 1), "48226158")
        self.assertEqual(fft("12345678", 2), "34040438")
        self.assertEqual(fft("12345678", 3), "03415518")
        self.assertEqual(fft("12345678", 4), "01029498")


if __name__ == '__main__':
    unittest.main()
