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


class FractureTest(unittest.TestCase):
    def setUp(self):
        self.segment = segmented_filaments.BasicSegment(False, 5)

    def test_fracture_middle(self):
        left, middle, right = self.segment.fracture(1, True)
        self.assertEqual(False, left.state)
        self.assertEqual(1, left.count)
        self.assertEqual(True, middle.state)
        self.assertEqual(1, middle.count)
        self.assertEqual(False, right.state)
        self.assertEqual(3, right.count)

    def test_fracture_left(self):
        left, right = self.segment.fracture(0, True)
        self.assertEqual(True, left.state)
        self.assertEqual(1, left.count)
        self.assertEqual(False, right.state)
        self.assertEqual(4, right.count)

    def test_fracture_right(self):
        left, right = self.segment.fracture(4, True)
        self.assertEqual(False, left.state)
        self.assertEqual(4, left.count)
        self.assertEqual(True, right.state)
        self.assertEqual(1, right.count)


class DecrementTest(unittest.TestCase):
    def setUp(self):
        self.segment = segmented_filaments.BasicSegment(None, 3)

    def test_decrement(self):
        new_segments = self.segment.decrement()
        self.assertEqual(2, new_segments[0].count)
        new_segments = new_segments[0].decrement()
        self.assertEqual(1, new_segments[0].count)
        self.assertEqual([], new_segments[0].decrement())


class MergeTest(unittest.TestCase):
    def setUp(self):
        self.segment_a_1 = segmented_filaments.BasicSegment('a', 3)
        self.segment_a_2 = segmented_filaments.BasicSegment('a', 1)
        self.segment_b_1 = segmented_filaments.BasicSegment('b', 2)

    def test_merge_same_states(self):
        new_segments = self.segment_a_1.merge(self.segment_a_2)
        self.assertEqual(1, len(new_segments))

        self.assertEqual('a', new_segments[0].state)
        self.assertEqual(4, new_segments[0].count)

    def test_merge_different_states(self):
        left, right = self.segment_a_1.merge(self.segment_b_1)

        self.assertEqual('a', left.state)
        self.assertEqual(3, left.count)

        self.assertEqual('b', right.state)
        self.assertEqual(2, right.count)


if '__main__' == __name__:
    unittest.main()
