import unittest
import collections

from hydro_sim.transitions import depolymerization

class MockConcentration(object):
    def remove_monomer(self):
        pass

    def add_monomer(self):
        pass

class MockState(object):
    def __init__(self):
        self.strand = []
        self.concentrations = {'t': MockConcentration(),
                               'd': MockConcentration(),
                               'n': MockConcentration()}

class FixedRateDepolymerizationTest(unittest.TestCase):
    def test_barbed(self):
        fr = depolymerization.Barbed('d', 2.2)

        state = MockState()
        state.strand = ['n']
        self.assertEqual(0, fr.R(state))

        state.strand.append('d')
        self.assertEqual(2.2, fr.R(state))

        state.strand.append('d')
        state.strand.append('d')
        self.assertEqual(2.2, fr.R(state))

        fr.perform(None, state, None)
        self.assertEqual(['n', 'd', 'd'], state.strand)
        self.assertEqual(2.2, fr.R(state))

        fr.perform(None, state, None)
        self.assertEqual(['n', 'd'], state.strand)
        self.assertEqual(2.2, fr.R(state))

        fr.perform(None, state, None)
        self.assertEqual(['n'], state.strand)
        self.assertEqual(0, fr.R(state))

if '__main__' == __name__:
    unittest.main()
