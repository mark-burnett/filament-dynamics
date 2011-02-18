import unittest
import collections

from actin_dynamics.primitives.filaments.single_strand_filaments import Filament
from actin_dynamics.primitives import concentrations

# This would be a decent test to adapt and add for good measure.
#        for s, l in self.state_indices.items():
#            assert(len(l) == self._sequence.count(s))
#            for i in l:
#                assert(s == self._sequence[i])

class FilamentTest(unittest.TestCase):
    def setUp(self):
        self.filament = Filament(['d', 'd', 'p', 't', 'p', 't', 't'])

    def tearDown(self):
        del self.filament


    def test_grow_barbed_end(self):
        self.filament.grow_barbed_end('p')

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't', 't', 'p'],
                         list(self.filament.states))

        # Verify state indices.
        self.assertEqual(3, self.filament.state_count('t'))
        self.assertEqual(3, self.filament.state_count('p'))
        self.assertEqual(2, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(2, self.filament.boundary_count('p', 't'))

    def test_shrink_barbed_end(self):
        self.filament.shrink_barbed_end()

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't'],
                         list(self.filament.states))

        # Verify state indices.
        self.assertEqual(2, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(2, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))

        # Pop again
        self.filament.shrink_barbed_end()

        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p'],
                         list(self.filament.states))

        # Verify state indices.
        self.assertEqual(1, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(2, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(1, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))


    def test_grow_pointed_end_getitem(self):
        self.filament.grow_pointed_end('p')

        # Verify sequence.
        new_sequence = ['p', 'd', 'd', 'p', 't', 'p', 't', 't']
        self.assertEqual(new_sequence, list(self.filament.states))

        # Test getitem
        for i, s in enumerate(new_sequence):
            self.assertEqual(s, self.filament[i])

        # Verify state indices.
        self.assertEqual(3, self.filament.state_count('t'))
        self.assertEqual(3, self.filament.state_count('p'))
        self.assertEqual(2, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))

    def test_grow_pointed_end_setitem(self):
        self.filament.grow_pointed_end('p')

        # Test setitem
        final_sequence = ['p', 'd', 'd', 'd', 't', 'p', 't', 't']
        self.filament[3] = 'd'
        self.assertEqual(final_sequence, list(self.filament.states))

        # Verify state indices.
        self.assertEqual(3, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(3, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(1, self.filament.boundary_count('t', 'p'))
        self.assertEqual(1, self.filament.boundary_count('t', 'd'))
        self.assertEqual(0, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))


    def test_shrink_pointed_end_getitem(self):
        self.filament.shrink_pointed_end()

        # Verify sequence.
        new_sequence = ['d', 'p', 't', 'p', 't', 't']
        self.assertEqual(new_sequence, list(self.filament.states))

        # Test getitem
        for i, s in enumerate(new_sequence):
            self.assertEqual(s, self.filament[i])

        # Verify state indices.
        self.assertEqual(3, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(1, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))

        # Second step
        self.filament.shrink_pointed_end()

        # Verify sequence.
        new_sequence = ['p', 't', 'p', 't', 't']
        self.assertEqual(new_sequence, list(self.filament.states))

        # Test getitem
        for i, s in enumerate(new_sequence):
            self.assertEqual(s, self.filament[i])

        # Verify state indices.
        self.assertEqual(3, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(0, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(0, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))

        # Barbed check
        self.filament.shrink_barbed_end()

        # Verify sequence.
        new_sequence = ['p', 't', 'p', 't']
        self.assertEqual(new_sequence, list(self.filament.states))

        # Verify state indices.
        self.assertEqual(2, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(0, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(0, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))


    def test_shrink_pointed_end_setitem(self):
        self.filament.shrink_pointed_end()

        # Setitem
        self.filament[2] = 'd'
        final_sequence = ['d', 'p', 'd', 'p', 't', 't']

        # Verify state indices.
        self.assertEqual(2, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(2, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(1, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(2, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('d', 'p'))
        self.assertEqual(0, self.filament.boundary_count('p', 't'))

        # Second step
        self.filament.shrink_pointed_end()

        # Setitem
        final_sequence = ['p', 'd', 'p', 't', 't']

        # Verify state indices.
        self.assertEqual(2, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(1, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(1, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('d', 'p'))
        self.assertEqual(0, self.filament.boundary_count('p', 't'))


    def test_grow_then_shrink_pointed_end(self):
        self.filament.grow_pointed_end('p')
        self.filament.shrink_pointed_end()

        new_states = ['d', 'd', 'p', 't', 'p', 't', 't']
        self.assertEqual(new_states, list(self.filament.states))


    def test_state_count(self):
        self.assertEqual(3, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(2, self.filament.state_count('d'))
        self.assertEqual(0, self.filament.state_count('z'))

    def test_boundary_count(self):
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))

        self.assertEqual(0, self.filament.boundary_count('y', 'z'))

    def test_non_boundary_state_count(self):
        self.assertEqual(1, self.filament.non_boundary_state_count('t', 'p'))
        self.assertEqual(1, self.filament.non_boundary_state_count('p', 'd'))
        self.assertEqual(3, self.filament.non_boundary_state_count('t', 'd'))
        self.assertEqual(2, self.filament.non_boundary_state_count('d', 'z'))


    def test_len(self):
        self.assertEqual(7, len(self.filament))

    def test_contains(self):
        self.assertTrue('t' in self.filament)
        self.assertTrue('p' in self.filament)
        self.assertTrue('d' in self.filament)

        self.assertFalse(None in self.filament)
        self.assertFalse(3 in self.filament)
        self.assertFalse('z' in self.filament)

    def test_getitem(self):
        for i, v in enumerate(['d', 'd', 'p', 't', 'p', 't', 't']):
            self.assertEqual(v, self.filament[i])

    def test_setitem_middle(self):
        self.filament[1] = 't'
        # Verify sequence.
        self.assertEqual(['d', 't', 'p', 't', 'p', 't', 't'],
                         list(self.filament.states))

        # Verify state indices.
        self.assertEqual(4, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(1, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(1, self.filament.boundary_count('t', 'd'))
        self.assertEqual(0, self.filament.boundary_count('p', 'd'))
        self.assertEqual(2, self.filament.boundary_count('p', 't'))

    def test_setitem_barbed(self):
        self.filament[-1] = 'd'
        # Verify sequence.
        self.assertEqual(['d', 'd', 'p', 't', 'p', 't', 'd'],
                         list(self.filament.states))

        # Verify state indices.
        self.assertEqual(2, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(3, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(1, self.filament.boundary_count('d', 't'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))

    def test_setitem_pointed(self):
        self.filament[0] = 'p'
        # Verify sequence.
        self.assertEqual(['p', 'd', 'p', 't', 'p', 't', 't'],
                         list(self.filament.states))

        # Verify state indices.
        self.assertEqual(3, self.filament.state_count('t'))
        self.assertEqual(3, self.filament.state_count('p'))
        self.assertEqual(1, self.filament.state_count('d'))

        # Verify boundary indices.
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(0, self.filament.boundary_count('t', 'd'))
        self.assertEqual(0, self.filament.boundary_count('d', 't'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('d', 'p'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))

if '__main__' == __name__:
    unittest.main()
