import unittest

from hydro_sim.transitions.hydrolysis import predicates
import hydro_sim.state

class PredicatesTest(unittest.TestCase):
    def test_random_full_count(self):
        initial_strand = ['t', 'd', 'p', 't', 'p', 'd', 'd', 'p', 'd']
        strand = hydro_sim.state.State(['t', 'p', 'd'], initial_strand, None)

        indices_t = [0, 3]
        indices_p = [2, 4, 7]
        indices_d = [1, 5, 6, 8]

        self.assertEqual(indices_t, strand.indices['t'])
        self.assertEqual(indices_p, strand.indices['p'])
        self.assertEqual(indices_d, strand.indices['d'])

        pred_t = predicates.Random('t')
        pred_p = predicates.Random('p')
        pred_d = predicates.Random('d')

        self.assertEqual(2, pred_t.full_count(strand))
        self.assertEqual(3, pred_p.full_count(strand))
        self.assertEqual(4, pred_d.full_count(strand))

    def test_random_update_vicinity(self):
        strand = ['t', 'd', 'p', 't', 'p', 'd', 'd', 'p', 'd']

        pred_p = predicates.Random('p')

        self.assertEqual( 1, pred_p.update_vicinity(2, strand, None))
        self.assertEqual( 0, pred_p.update_vicinity(3, strand, None))
        self.assertEqual(-1, pred_p.update_vicinity(1, strand, 'p'))

    def test_pointed_neighbor_full_count(self):
        initial_strand = ['t', 'd', 'p', 't', 'p', 'd', 'd', 'p', 'd']
        strand = hydro_sim.state.State(['t', 'p', 'd'], initial_strand, None)

        pred_tp = predicates.PointedNeighbor('t', 'p')
        pred_pd = predicates.PointedNeighbor('p', 'd')
        pred_dp = predicates.PointedNeighbor('d', 'p')

        self.assertEqual(1, pred_tp.full_count(strand))
        self.assertEqual(2, pred_pd.full_count(strand))
        self.assertEqual(2, pred_dp.full_count(strand))

    def test_pointed_neighbor_update_vicinity(self):
        strand = ['t', 'd', 'p', 't', 'p', 'd', 'd', 'p', 'd', 'd']

        pred_pd = predicates.PointedNeighbor('p', 'd')

        # Add one
        self.assertEqual( 1, pred_pd.update_vicinity(2, strand, None))
        self.assertEqual( 1, pred_pd.update_vicinity(1, strand, 'p'))

        # No change
        self.assertEqual( 0, pred_pd.update_vicinity(4, strand, 't'))
        self.assertEqual( 0, pred_pd.update_vicinity(5, strand, 'p'))

        # Add one and subtract one
        self.assertEqual( 0, pred_pd.update_vicinity(6, strand, 'p'))

        # Subtract one
        self.assertEqual(-1, pred_pd.update_vicinity(3, strand, 'd'))
        self.assertEqual(-1, pred_pd.update_vicinity(9, strand, 'p'))

if '__main__' == __name__:
    unittest.main()
