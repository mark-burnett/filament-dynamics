import unittest
import collections

from actin_dynamics.simulation.strand_factories import strands
from actin_dynamics.simulation import concentrations

# This would be a decent test to adapt and add for good measure.
#        # XXX DEBUG debug
#        for s, l in self.state_indices.items():
#            assert(len(l) == self._sequence.count(s))
#            for i in l:
#                assert(s == self._sequence[i])

class StrandTest(unittest.TestCase):
    def setUp(self):
        self.strand = strands.single_strand.Strand(['d', 'd', 'p', 't', 'p', 't', 't'])

    def tearDown(self):
        del self.strand

    def test_initial_state(self):
        # Verify state indices.
        self.assertEqual(3, len(self.strand.state_indices['t']))
        self.assertEqual(2, len(self.strand.state_indices['p']))
        self.assertEqual(2, len(self.strand.state_indices['d']))

        # Verify boundary indices.
        self.assertEqual(2, len(self.strand.boundary_indices['t']['p']))
        self.assertEqual(0, len(self.strand.boundary_indices['t']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['t']))

    def test_grow_barbed_end(self):
        self.strand.grow_barbed_end('p')

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't', 't', 'p'],
                         self.strand.states)

        # Verify state indices.
        self.assertEqual(3, len(self.strand.state_indices['t']))
        self.assertEqual(3, len(self.strand.state_indices['p']))
        self.assertEqual(2, len(self.strand.state_indices['d']))

        # Verify boundary indices.
        self.assertEqual(2, len(self.strand.boundary_indices['t']['p']))
        self.assertEqual(0, len(self.strand.boundary_indices['t']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['d']))
        self.assertEqual(2, len(self.strand.boundary_indices['p']['t']))

    def test_shrink_barbed_end(self):
        self.strand.shrink_barbed_end()

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't'], self.strand.states)

        # Verify state indices.
        self.assertEqual(2, len(self.strand.state_indices['t']))
        self.assertEqual(2, len(self.strand.state_indices['p']))
        self.assertEqual(2, len(self.strand.state_indices['d']))

        # Verify boundary indices.
        self.assertEqual(2, len(self.strand.boundary_indices['t']['p']))
        self.assertEqual(0, len(self.strand.boundary_indices['t']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['t']))

        # Pop again
        self.strand.shrink_barbed_end()

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p'], self.strand.states)

        # Verify state indices.
        self.assertEqual(1, len(self.strand.state_indices['t']))
        self.assertEqual(2, len(self.strand.state_indices['p']))
        self.assertEqual(2, len(self.strand.state_indices['d']))

        # Verify boundary indices.
        self.assertEqual(1, len(self.strand.boundary_indices['t']['p']))
        self.assertEqual(0, len(self.strand.boundary_indices['t']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['t']))

    def test_getitem(self):
        for i, v in enumerate(['d', 'd', 'p', 't', 'p', 't', 't']):
            self.assertEqual(v, self.strand[i])

    def test_setitem_middle(self):
        self.strand[1] = 't'
        # Verify sequence.
        self.assertEqual(['d', 't', 'p', 't', 'p', 't', 't'],
                         self.strand.states)

        # Verify state indices.
        self.assertEqual(4, len(self.strand.state_indices['t']))
        self.assertEqual(2, len(self.strand.state_indices['p']))
        self.assertEqual(1, len(self.strand.state_indices['d']))

        # Verify boundary indices.
        self.assertEqual(2, len(self.strand.boundary_indices['t']['p']))
        self.assertEqual(1, len(self.strand.boundary_indices['t']['d']))
        self.assertEqual(0, len(self.strand.boundary_indices['p']['d']))
        self.assertEqual(2, len(self.strand.boundary_indices['p']['t']))

    def test_setitem_barbed(self):
        self.strand[-1] = 'd'
        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't', 'd'],
                         self.strand.states)

        # Verify state indices.
        self.assertEqual(2, len(self.strand.state_indices['t']))
        self.assertEqual(2, len(self.strand.state_indices['p']))
        self.assertEqual(3, len(self.strand.state_indices['d']))

        # Verify boundary indices.
        self.assertEqual(2, len(self.strand.boundary_indices['t']['p']))
        self.assertEqual(0, len(self.strand.boundary_indices['t']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['d']['t']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['t']))

    def test_setitem_pointed(self):
        self.strand[0] = 'p'
        # Verify sequence.
        self.assertEqual(['p', 'd', 'p', 't', 'p', 't', 't'],
                         self.strand.states)

        # Verify state indices.
        self.assertEqual(3, len(self.strand.state_indices['t']))
        self.assertEqual(3, len(self.strand.state_indices['p']))
        self.assertEqual(1, len(self.strand.state_indices['d']))

        # Verify boundary indices.
        self.assertEqual(2, len(self.strand.boundary_indices['t']['p']))
        self.assertEqual(0, len(self.strand.boundary_indices['t']['d']))
        self.assertEqual(0, len(self.strand.boundary_indices['d']['t']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['d']['p']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['t']))

if '__main__' == __name__:
    unittest.main()
