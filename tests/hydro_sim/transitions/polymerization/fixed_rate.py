import unittest
import collections

from util import observer
from hydro_sim.transitions import events
from hydro_sim.transitions.polymerization import fixed_rate

class MockConcentration(object):
    def __init__(self, value):
        self.value        = value
        self.initialized  = False
        self.poly_count   = 0
        self.depoly_count = 0

    def initialize(self):
        self.initialized = True

    def __call__(self):
        return self.value

    def update_poly(self, event):
        self.poly_count += 1

    def update_depoly(self, event):
        self.depoly_count += 1

class FixedRatePolymerizationTest(unittest.TestCase):
    def test_barbed(self):
        concentration = MockConcentration(7)
        fr = fixed_rate.Barbed({'t': concentration}, 't', 0.3)
        self.assertFalse(concentration.initialized)

        pub = observer.Publisher()
        strand = []

        fr.initialize(pub, strand)
        self.assertTrue(concentration.initialized)
        self.assertEqual(7*0.3, fr.R)

        self.assertEqual(0, concentration.poly_count)
        self.assertEqual(0, concentration.depoly_count)

        fr.perform(None, None)
        self.assertEqual(7*0.3, fr.R)
        self.assertEqual(['t'], strand)
        self.assertEqual(1, concentration.poly_count)
        self.assertEqual(0, concentration.depoly_count)

        fr.perform(None, None)
        self.assertEqual(7*0.3, fr.R)
        self.assertEqual(['t', 't'], strand)
        self.assertEqual(2, concentration.poly_count)
        self.assertEqual(0, concentration.depoly_count)

    def test_pointed(self):
        concentration = MockConcentration(7)
        fr = fixed_rate.Pointed({'t': concentration}, 't', 0.3)
        self.assertFalse(concentration.initialized)

        pub = observer.Publisher()
        strand = collections.deque()

        fr.initialize(pub, strand)
        self.assertTrue(concentration.initialized)
        self.assertEqual(7*0.3, fr.R)

        self.assertEqual(0, concentration.poly_count)
        self.assertEqual(0, concentration.depoly_count)

        fr.perform(None, None)
        self.assertEqual(7*0.3, fr.R)
        self.assertEqual(collections.deque(['t']), strand)
        self.assertEqual(1, concentration.poly_count)
        self.assertEqual(0, concentration.depoly_count)

        fr.perform(None, None)
        self.assertEqual(7*0.3, fr.R)
        self.assertEqual(collections.deque(['t', 't']), strand)
        self.assertEqual(2, concentration.poly_count)
        self.assertEqual(0, concentration.depoly_count)



if '__main__' == __name__:
    unittest.main()
