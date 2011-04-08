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

import itertools
from actin_dynamics.state import edge_tracking_filaments

def _iterate_pairs(lst):
    right = iter(lst)
    right.next() # skip one!
    left  = iter(lst)
    return itertools.izip(left, right)

def naive_boundary_count(states, barbed, pointed):
    target = (pointed, barbed)
    count = 0
    for current in _iterate_pairs(states):
        if current == target:
            count += 1
    return count

class EdgeFilamentTest(unittest.TestCase):
    def setUp(self):
        self.states = ['d', 'd', 'p', 't', 'p', 't', 't']
        self.filament = edge_tracking_filaments.EdgeTrackingFilament.from_iterable(
                self.states)

    def test_construction(self):
        self.assertEqual(['d', 'p', 't', 'p', 't'], list(self.filament._states))
        self.assertEqual([2, 1, 1, 1, 2], list(self.filament._counts))
        self.assertEqual([2, 3, 4, 5, 7], list(self.filament._edges))

    def check_filament(self):
        self.test_iter()
        self.test_getitem()
        self.test_state_count()
        self.test_boundary_count()

    def test_iter(self):
        self.assertEqual(self.states, list(self.filament))

    def test_state_count(self):
        self.assertEqual(self.states.count('t'), self.filament.state_count('t'))
        self.assertEqual(self.states.count('p'), self.filament.state_count('p'))
        self.assertEqual(self.states.count('d'), self.filament.state_count('d'))

    def test_boundary_count(self):
        self.assertEqual(naive_boundary_count(self.states, 't', 'p'),
                         self.filament.boundary_count('t', 'p'))
        self.assertEqual(naive_boundary_count(self.states, 'p', 'd'),
                         self.filament.boundary_count('p', 'd'))
        self.assertEqual(naive_boundary_count(self.states, 'p', 't'),
                         self.filament.boundary_count('p', 't'))
        self.assertEqual(naive_boundary_count(self.states, 'd', 'p'),
                         self.filament.boundary_count('d', 'p'))

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

    def test_getitem(self):
        for i, state in enumerate(self.states):
            self.assertEqual(state, self.filament[i])

    def test_negative_getitem(self):
        for i in xrange(len(self.states)):
            self.assertEqual(self.states[-(i+1)], self.filament[-(i+1)])

    def test_setitem(self):
        # single
        self.filament[2] = 'd'
        self.states[2]   = 'd'
        self.assertEqual(['d', 't', 'p', 't'], list(self.filament._states))
        self.check_filament()

        # left edge
        self.filament[5] = 'p'
        self.states[5]   = 'p'
        self.assertEqual(['d', 't', 'p', 't'], list(self.filament._states))
        self.test_iter()
        self.check_filament()

        # middle
        self.filament[1] = 't'
        self.states[1]   = 't'
        self.assertEqual(['d', 't', 'd', 't', 'p', 't'],
                         list(self.filament._states))
        self.check_filament()

        # right edge
        self.filament[5] = 'd'
        self.states[5]   = 'd'
        self.assertEqual(['d', 't', 'd', 't', 'p', 'd', 't'],
                         list(self.filament._states))
        self.check_filament()

        # tip, non merging
        self.filament[-1] = 'p'
        self.states[-1]   = 'p'
        self.assertEqual(['d', 't', 'd', 't', 'p', 'd', 'p'],
                         list(self.filament._states))
        self.check_filament()

        # tip, merging
        self.filament[-1] = 'd'
        self.states[-1]   = 'd'
        self.assertEqual(['d', 't', 'd', 't', 'p', 'd'],
                         list(self.filament._states))
        self.check_filament()

        # base, non merging
        self.filament[0] = 'p'
        self.states[0]   = 'p'
        self.assertEqual(['p', 't', 'd', 't', 'p', 'd'],
                         list(self.filament._states))
        self.check_filament()

        # base, merging
        self.filament[0] = 't'
        self.states[0]   = 't'
        self.assertEqual(['t', 'd', 't', 'p', 'd'],
                         list(self.filament._states))
        self.check_filament()

        # another merge
        self.filament[2] = 't'
        self.states[2]   = 't'
        self.assertEqual(['t', 'p', 'd'],
                         list(self.filament._states))
        self.check_filament()


    def test_grow_barbed_end(self):
        self.filament.grow_barbed_end('t')
        self.states.append('t')
        self.check_filament()
        self.assertEqual(4, self.filament.state_count('t'))

        self.filament.grow_barbed_end('d')
        self.states.append('d')
        self.check_filament()
        self.assertEqual(3, self.filament.state_count('d'))

        self.filament.grow_barbed_end('t')
        self.states.append('t')
        self.check_filament()
        self.assertEqual(5, self.filament.state_count('t'))

    def test_grow_pointed_end(self):
        self.filament.grow_pointed_end('d')
        self.states.insert(0, 'd')
        self.check_filament()
        self.assertEqual(3, self.filament.state_count('d'))


        self.filament.grow_pointed_end('p')
        self.states.insert(0, 'p')
        self.check_filament()
        self.assertEqual(3, self.filament.state_count('p'))

        self.filament.grow_pointed_end('t')
        self.states.insert(0, 't')
        self.check_filament()
        self.assertEqual(4, self.filament.state_count('t'))

    def test_shrink_barbed_end(self):
        self.filament.shrink_barbed_end()
        self.states.pop()
        self.check_filament()

        self.filament.shrink_barbed_end()
        self.states.pop()
        self.check_filament()

    def test_shrink_pointed_end(self):
        self.filament.shrink_pointed_end()
        del self.states[0]
        self.check_filament()

        self.filament.shrink_pointed_end()
        del self.states[0]
        self.check_filament()

    def test_merge_neighbors_left(self):
        self.filament._states[1] = 'd'
        self.filament._merge_neighbors(1)
        self.assertEqual(list(self.filament._states), ['d', 't', 'p', 't'])

    def test_merge_neighbors_middle(self):
        self.filament._states[2] = 'p'
        self.filament._merge_neighbors(2)
        self.assertEqual(list(self.filament._states), ['d', 'p', 't'])

    def test_merge_neighbors_right(self):
        self.filament._states[1] = 't'
        self.filament._merge_neighbors(1)
        self.assertEqual(list(self.filament._states), ['d', 't', 'p', 't'])

    def test_merge_neighbors_none(self):
        self.filament._states[3] = 'd'
        self.filament._merge_neighbors(3)
        self.assertEqual(['d', 'p', 't', 'd', 't'], list(self.filament._states))

    def test_get_containing_segment(self):
        self.assertEqual(0, self.filament._get_containing_segment(0))
        self.assertEqual(0, self.filament._get_containing_segment(1))
        self.assertEqual(1, self.filament._get_containing_segment(2))
        self.assertEqual(2, self.filament._get_containing_segment(3))
        self.assertEqual(4, self.filament._get_containing_segment(6))


if '__main__' == __name__:
    unittest.main()
