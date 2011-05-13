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

from actin_dynamics.numerical import collate

from actin_dynamics import database


class GetTimesTest(unittest.TestCase):
    def setUp(self):
        self.flat_data = [[[3, 4, 5], None],
                          [[3, 4], None],
                          [[0, 1], None],
                          [[7, 8], None]]

        self.times = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def test_get_times(self):
        self.assertEqual(self.times, collate.get_times(self.flat_data))


class CollateDataTest(unittest.TestCase):
    def setUp(self):
        self.flat_data = [(range(3), [2, 1, 0]),
                (range(2), [1, 0]), (range(2), [1, 0]),
                (range(3), [2, 1, 0])]
        self.times = map(float, range(3))
        self.collated_data = [[2, 1, 1, 2], [1, 0, 0, 1], [0, 0]]

    def test_collate(self):
        self.assertEqual((self.times, self.collated_data),
                collate.collate_on_times(self.flat_data))


if '__main__' == __name__:
    unittest.main()

