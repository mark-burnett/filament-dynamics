import unittest

from kmc import end_conditions

class DurationTest(unittest.TestCase):
    def test_normal_duration(self):
        d = end_conditions.Duration(17)
        self.assertFalse(d(0,  None))
        self.assertFalse(d(5,  None))
        self.assertFalse(d(16, None))
        self.assertFalse(d(17, None))
        self.assertTrue(d( 18, None))
        self.assertTrue(d(131, None))
    
    def test_zero_duration(self):
        self.assertRaises(ValueError, end_conditions.Duration, 0)

    def test_negative_duration(self):
        self.assertRaises(ValueError, end_conditions.Duration, -1)
        self.assertRaises(ValueError, end_conditions.Duration, -17)

class RandomDurationTest(unittest.TestCase):
    def test_normal_duration(self):
        durations = [20, 6, 107, 85.0]
        for d in durations:
            rd = end_conditions.RandomDuration(d)
            rd.reset()
            self.assertTrue(rd.duration < d)

            cd = rd.duration
            self.assertFalse(rd(cd - 1, None))
            self.assertTrue( rd(cd + 1, None))
            self.assertFalse(rd(float(cd)/2, None))
            self.assertTrue( rd(float(cd)*2, None))

            self.assertTrue(rd(d, None))

    def test_zero_duration(self):
        self.assertRaises(ValueError, end_conditions.RandomDuration, 0)

    def test_negative_duration(self):
        self.assertRaises(ValueError, end_conditions.RandomDuration, -1)
        self.assertRaises(ValueError, end_conditions.RandomDuration, -17)

class StateLengthBelowTest(unittest.TestCase):
    def test_vary_state(self):
        lengths     = [0, 5, 6, 7, 12]
        expectation = [True, True, False, False, False]
        ec = end_conditions.StateLengthBelow(6)
        for l, e in zip(lengths, expectation):
            self.assertEqual(e, ec(None, range(l)))

    def test_vary_condition(self):
        lengths     = [0, 5, 6, 7, 12]
        expectation = [False, False, False, True, True]
        state = range(6)
        for l, e in zip(lengths, expectation):
            ec = end_conditions.StateLengthBelow(l)
            self.assertEqual(e, ec(None, state))

if '__main__' == __name__:
    unittest.main()
