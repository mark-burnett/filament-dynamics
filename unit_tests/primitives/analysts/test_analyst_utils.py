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

from actin_dynamics.primitives.analysts import analyst_utils

from actin_dynamics import database

class FlattenDataTest(unittest.TestCase):
    def setUp(self):
        self.raw_data = [{'A': range(3), 'B': range(2)},
                         {'C': range(2), 'D': range(3)}]
        self.flat_data = [range(3), range(2), range(2), range(3)]

    def test_already_flat(self):
        self.assertEqual(self.flat_data,
                analyst_utils.flatten_data(self.flat_data))

    def test_flatten(self):
        self.assertEqual(self.flat_data,
                analyst_utils.flatten_data(self.raw_data))


class GetTimesTest(unittest.TestCase):
    def setUp(self):
        self.flat_data = [[[3, 4, 5], None],
                          [[3, 4], None],
                          [[0, 1], None],
                          [[7, 8], None]]

        self.times = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def test_get_times(self):
        self.assertEqual(self.times, analyst_utils.get_times(self.flat_data))


class CollateDataTest(unittest.TestCase):
    def setUp(self):
        self.raw_data = [{'A': [range(3), list(reversed(range(3)))],
                          'B': [range(2), list(reversed(range(2)))]},
                         {'C': [range(2), list(reversed(range(2)))],
                          'D': [range(3), list(reversed(range(3)))]}]
        self.flat_data = [range(3), range(2), range(2), range(3)]
        self.times = range(3)
        self.collated_data = [[2, 1, 1, 2], [1, 0, 0, 1], [0, 0]]

    def test_collate(self):
        self.assertEqual((self.times, self.collated_data),
                analyst_utils.collate_data(self.raw_data))


if '__main__' == __name__:
    unittest.main()
