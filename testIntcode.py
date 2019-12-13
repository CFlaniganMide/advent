import unittest

from intcode import Intcode


class MyTestCase(unittest.TestCase):
    def test_day2(self):

        programStr = "1,9,10,3,2,3,11,0,99,30,40,50"
        computer = Intcode(programStr)
        computer.run()
        self.assertEqual(computer.program[0], 3500)

    def test_day5(self):
        programStr = "3,0,4,0,99"
        computer = Intcode(programStr)
        input = [1]
        output = computer.run(input)
        self.assertEqual(output, 1)

    def test_day7(self):
        programStr = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
        computer = Intcode(programStr)
        phase = [4,3,2,1,0]
        input = [0]
        for i, p in enumerate(phase):
            input.append(computer.run([p, input[i]]))
        self.assertEqual(input[-1], 43210)

        programStr = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
        computer = Intcode(programStr)
        phase = [0,1,2,3,4]
        input = [0]
        for i, p in enumerate(phase):
            input.append(computer.run([p, input[i]]))
        self.assertEqual(input[-1], 54321)

        programStr = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
        computer = Intcode(programStr)
        phase = [1,0,4,3,2]
        input = [0]
        for i, p in enumerate(phase):
            input.append(computer.run([p, input[i]]))
        self.assertEqual(input[-1], 65210)


if __name__ == '__main__':
    unittest.main()
