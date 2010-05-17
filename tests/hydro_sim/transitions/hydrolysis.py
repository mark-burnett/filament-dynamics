import unittest
import collections

from hydro_sim import concentrations
from hydro_sim.transitions import hydrolysis

from hydro_sim import strand

class RandomHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.strand = strand.Strand(['t', 'p', 'd'],
                                    ['d', 'd', 'p', 't', 'p', 't', 't'],
                                    collections.defaultdict(
                                        concentrations.ZeroConcentration))
        self.tp_transition = hydrolysis.Random('t', 1,   'p')
        self.pd_transition = hydrolysis.Random('p', 0.5, 'd')

    def tearDown(self):
        del self.strand
        del self.tp_transition
        del self.pd_transition

    def test_R(self):
        self.assertEqual(3, self.tp_transition.R(self.strand))
        self.assertEqual(1, self.pd_transition.R(self.strand))

    def test_perform(self):
        self.tp_transition.perform(None, self.strand, 1.5)
        for i, v in enumerate(['d', 'd', 'p', 't', 'p', 'p', 't']):
            self.assertEqual(v, self.strand[i])

        self.pd_transition.perform(None, self.strand, 0)
        for i, v in enumerate(['d', 'd', 'd', 't', 'p', 'p', 't']):
            self.assertEqual(v, self.strand[i])

class PointedNeighborHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.strand = strand.Strand(['t', 'p', 'd'],
                                    ['d', 'd', 'p', 't', 'p', 't', 't'],
                                    collections.defaultdict(
                                        concentrations.ZeroConcentration))
        self.tp_transition = hydrolysis.PointedNeighbor('t', 'p', 1,   'p')
        self.pd_transition = hydrolysis.PointedNeighbor('p', 'd', 0.5, 'd')

    def tearDown(self):
        del self.strand
        del self.tp_transition
        del self.pd_transition

    def test_R(self):
        self.assertEqual(2,   self.tp_transition.R(self.strand))
        self.assertEqual(0.5, self.pd_transition.R(self.strand))

    def test_perform(self):
        self.tp_transition.perform(None, self.strand, 1.5)
        for i, v in enumerate(['d', 'd', 'p', 't', 'p', 'p', 't']):
            self.assertEqual(v, self.strand[i])

        self.pd_transition.perform(None, self.strand, 0)
        for i, v in enumerate(['d', 'd', 'd', 't', 'p', 'p', 't']):
            self.assertEqual(v, self.strand[i])

if '__main__' == __name__:
    unittest.main()
