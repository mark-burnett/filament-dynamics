import unittest

from hydro_sim import measurements

class MockState(object):
    def __init__(self, strand):
        self.strand = strand

class LengthTest(unittest.TestCase):
    def test_normal_use(self):
        times  = [1, 2, 3, 4]
        lengths = [3, 7, 8, 1]

        m = measurements.StrandLength('mylabel')
        self.assertEqual('mylabel', m.label)

        for t, l in zip(times, lengths):
            m.perform(t, MockState(range(l)))

        self.assertEqual(len(times), len(m.data))
        
        for t, l, d in zip(times, lengths, m.data):
            self.assertEqual((t, l), d)

if '__main__' == __name__:
    unittest.main()
