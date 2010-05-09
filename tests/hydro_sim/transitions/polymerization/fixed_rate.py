import unittest
import collections

from util import observer
from hydro_sim.transitions.polymerization import fixed_rate

class MockConcentration(object):
    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value

class MockPublisher(object):
    def subscribe(self, a, b):
        pass

class MockStrand(list):
    pass

class FixedRatePolymerizationTest(unittest.TestCase):
    def test_barbed(self):

        fr = fixed_rate.Barbed('t', 0.3)

        fr.initialize(MockPublisher(), None)

        strand = MockStrand()
        strand.concentrations = {'t': MockConcentration(7)}
        self.assertEqual(7*0.3, fr.R(strand))

        fr.perform(None, strand, None)
        self.assertEqual(7*0.3, fr.R(strand))
        self.assertEqual(['t'], strand)

        fr.perform(None, strand, None)
        self.assertEqual(7*0.3, fr.R(strand))
        self.assertEqual(['t', 't'], strand)

if '__main__' == __name__:
    unittest.main()
