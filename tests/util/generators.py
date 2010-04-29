import unittest
from util import generators

class RunningTotalTest(unittest.TestCase):
    def test_running_total(self):
        test_data = [[0, 1, 2, 3, 4, 5],
                     [7, 1, 2, 8],
                     [-5, 0, -2, 3]]
        answers   = [[0, 1, 3, 6, 10, 15],
                     [7, 8, 10, 18],
                     [-5, -5, -7, -4]]
        for a, d in zip(answers, test_data):
            self.assertEqual(a, list(generators.running_total(d)))

if '__main__' == __name__:
    unittest.main()
