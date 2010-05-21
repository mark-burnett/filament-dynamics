import unittest
import collections

from hydro_sim import strand
from hydro_sim import concentrations

# This would be a decent test to adapt and add for good measure.
#        # XXX DEBUG debug
#        for s, l in self.state_indices.items():
#            assert(len(l) == self._sequence.count(s))
#            for i in l:
#                assert(s == self._sequence[i])

class StrandTest(unittest.TestCase):
    def setUp(self):
        self.strand = strand.Strand(['t', 'p', 'd'],
                                    ['d', 'd', 'p', 't', 'p', 't', 't'])

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

    def test_append(self):
        self.strand.append('p')

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't', 't', 'p'], self.strand)

        # Verify state indices.
        self.assertEqual(3, len(self.strand.state_indices['t']))
        self.assertEqual(3, len(self.strand.state_indices['p']))
        self.assertEqual(2, len(self.strand.state_indices['d']))

        # Verify boundary indices.
        self.assertEqual(2, len(self.strand.boundary_indices['t']['p']))
        self.assertEqual(0, len(self.strand.boundary_indices['t']['d']))
        self.assertEqual(1, len(self.strand.boundary_indices['p']['d']))
        self.assertEqual(2, len(self.strand.boundary_indices['p']['t']))

    def test_pop(self):
        self.strand.pop()

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't'], self.strand)

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
        self.strand.pop()

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p'], self.strand)

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
        self.assertEqual(['d', 't', 'p', 't', 'p', 't', 't'], self.strand)

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
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't', 'd'], self.strand)

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
        self.assertEqual(['p', 'd', 'p', 't', 'p', 't', 't'], self.strand)

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


class StrandFactoryTest(unittest.TestCase):
    def test_typical_single_state_factory(self):
        strand_generator = strand.single_state(state='t2', length=7)
        for i in xrange(10):
            self.assertEqual(['t2']*7, next(strand_generator))

if '__main__' == __name__:
    unittest.main()
