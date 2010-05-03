import unittest
from util import functional

def mul_by_2(a):
    return 2 * a

def add_1(a):
    return a + 1

def sub_1(a):
    return a - 1

class ComposeTest(unittest.TestCase):
    def test_compose(self):
        sequences = map(functional.compose,
                        [[mul_by_2, add_1, mul_by_2, sub_1, mul_by_2],
                         [add_1, mul_by_2, sub_1],
                         [sub_1, mul_by_2, sub_1, mul_by_2, add_1]])
        starting_values = [6, 7, 1, 0, -1]
        ending_values   = [[50, 13, 19],
                           [58, 15, 23],
                           [10,  3, -1],
                           [ 2,  1, -5],
                           [-6, -1, -9]]

        for start, evs in zip(starting_values, ending_values):
            for c, end in zip(sequences, evs):
                self.assertEqual(end, c(start))

def suite():
    s = unittest.TestSuite()
    s.addTest(ComposeTest('test_compose'))
    return s

if '__main__' == __name__:
    unittest.main()
