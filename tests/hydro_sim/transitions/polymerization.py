import unittest
import collections

from util import observer
from hydro_sim.transitions import polymerization

class MockConcentration(object):
    def __init__(self, value):
        self.value = value

    def remove_monomer(self):
        pass

    def add_monomer(self):
        pass

class MockState(object):
    def __init__(self):
        self.strand = []
#        self.concentrations = collections.defaultdict(MockConcentration)

class FixedRatePolymerizationTest(unittest.TestCase):
    def test_barbed(self):
        fr = polymerization.Barbed('t', 0.3)

        state = MockState()
        state.concentrations = {'t': MockConcentration(7)}
        self.assertEqual(7*0.3, fr.R(state))

        fr.perform(None, state, None)
        self.assertEqual(7*0.3, fr.R(state))
        self.assertEqual(['t'], state.strand)

        fr.perform(None, state, None)
        self.assertEqual(7*0.3, fr.R(state))
        self.assertEqual(['t', 't'], state.strand)

if '__main__' == __name__:
    unittest.main()
