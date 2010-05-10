import unittest
import collections

from util import observer
from hydro_sim.transitions import polymerization

class MockConcentration(object):
    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value

class MockStrand(list):
    pass

class FixedRatePolymerizationTest(unittest.TestCase):
    def test_barbed(self):
        fr = polymerization.Barbed('t', 0.3)

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
