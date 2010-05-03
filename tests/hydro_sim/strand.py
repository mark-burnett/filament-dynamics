import unittest

from hydro_sim import strand

class StrandTest(unittest.TestCase):
    def test_typical_single_state_factory(self):
        strand_generator = strand.single_state(['t1', 't2'], ['t2', 't3'], 7)
        for i in xrange(10):
            self.assertEqual(['t2']*7, next(strand_generator))

if '__main__' == __name__:
    unittest.main()
