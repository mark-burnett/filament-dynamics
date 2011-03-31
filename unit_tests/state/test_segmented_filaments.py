#    Copyright (C) 2011 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from actin_dynamics.state import segmented_filaments

class SegmentedFilamentTest(unittest.TestCase):
    def setUp(self):
        self.states = ['d', 'd', 'p', 't', 'p', 't', 't']
        self.filament = segmented_filaments.SegmentedFilament.from_iterable(self.states)

    def test_iter(self):
        self.assertEqual(self.states, list(self.filament))

    def test_state_count(self):
        self.assertEqual(3, self.filament.state_count('t'))
        self.assertEqual(2, self.filament.state_count('p'))
        self.assertEqual(2, self.filament.state_count('d'))

    def test_boundary_count(self):
        self.assertEqual(2, self.filament.boundary_count('t', 'p'))
        self.assertEqual(1, self.filament.boundary_count('p', 'd'))
        self.assertEqual(1, self.filament.boundary_count('p', 't'))

    def test_len(self):
        self.assertEqual(len(self.states), len(self.filament))


    def test_state_index(self):
        self.assertEqual(2, self.filament.state_index('p', 0))
        self.assertEqual(1, self.filament.state_index('d', 1))
        self.assertEqual(6, self.filament.state_index('t', 2))

    def test_boundary_index(self):
        self.assertEqual(4, self.filament.boundary_index('p', 't', 0))
        self.assertEqual(2, self.filament.boundary_index('p', 'd', 0))
        self.assertEqual(5, self.filament.boundary_index('t', 'p', 1))

#    def test_non_boundary_state_count(self):
#        self.assertEqual(6, self.filament.non_boundary_state_index('t', 'p', 0))
#        self.assertEqual(5, self.filament.non_boundary_state_index('t', 'd', 1))
#        self.assertEqual(6, self.filament.non_boundary_state_index('t', 'd', 2))
#        self.assertEqual(2, self.filament.non_boundary_state_index('p', 't', 0))
#        self.assertEqual(4, self.filament.non_boundary_state_index('p', 'd', 0))

    def test_getitem(self):
        for i, state in enumerate(self.states):
            self.assertEqual(state, self.filament[i])

    def test_negative_getitem(self):
        for i in xrange(len(self.states)):
            self.assertEqual(self.states[-(i+1)], self.filament[-(i+1)])

    def test_setitem(self):
        self.filament[2] = 'd'
        self.states[2]   = 'd'
        self.test_getitem()

        self.filament[5] = 'p'
        self.states[5]   = 'p'
        self.test_getitem()

    def test_grow_barbed_end(self):
        self.filament.grow_barbed_end('t')
        self.states.append('t')
        self.test_getitem()

        self.filament.grow_barbed_end('d')
        self.states.append('d')
        self.test_getitem()

        self.filament.grow_barbed_end('t')
        self.states.append('t')
        self.test_getitem()

    def test_grow_pointed_end(self):
        self.filament.grow_pointed_end('d')
        self.states.insert(0, 'd')
        self.test_getitem()

        self.filament.grow_pointed_end('p')
        self.states.insert(0, 'p')
        self.test_getitem()

        self.filament.grow_pointed_end('t')
        self.states.insert(0, 't')
        self.test_getitem()

    def test_shrink_barbed_end(self):
        self.filament.shrink_barbed_end()
        self.states.pop()
        self.test_getitem()

        self.filament.shrink_barbed_end()
        self.states.pop()
        self.test_getitem()

    def test_shrink_pointed_end(self):
        self.filament.shrink_pointed_end()
        del self.states[0]
        self.test_getitem()

        self.filament.shrink_pointed_end()
        del self.states[0]
        self.test_getitem()

class CooperativeHydrolysisBugTest(unittest.TestCase):
    def setUp(self):
        self.states = ['d', 'd', 'p', 'p', 'p', 't', 't']
        self.filament = segmented_filaments.SegmentedFilament.from_iterable(self.states)

    def test_middle_merge(self):
        self.filament[3] = 'd'
        self.states[3] = 'd'
        self.assertEqual(self.states, list(self.filament))

    def test_left_boundary_inactive_merge(self):
        self.filament[2] = 't'
        self.states[2] = 't'
        self.assertEqual(self.states, list(self.filament))

    def test_left_boundary_active_merge(self):
        self.filament[2] = 'd'
        self.states[2] = 'd'
        self.assertEqual(self.states, list(self.filament))

    def test_right_boundary_inactive_merge(self):
        self.filament[4] = 'd'
        self.states[4] = 'd'
        self.assertEqual(self.states, list(self.filament))

    def test_right_boundary_active_merge(self):
        self.filament[4] = 't'
        self.states[4] = 't'
        self.assertEqual(self.states, list(self.filament))

    def test_pointed_end_merge(self):
        self.filament[0] = 'p'
        self.states[0] = 'p'
        self.assertEqual(self.states, list(self.filament))

    def test_barbed_end_merge(self):
        self.filament[-1] = 'p'
        self.states[-1] = 'p'
        self.assertEqual(self.states, list(self.filament))


if '__main__' == __name__:
    unittest.main()
