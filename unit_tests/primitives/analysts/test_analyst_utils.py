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




#class SEMTest(unittest.TestCase):
#    def setUp(self):
#        self.collated_data = [[2, 1, 1, 2], [1, 0, 0, 1], [0, 0]]
#
#    def test_collate_noscale_noadd(self):
#        means = [1.5, 0.5, 0]
#        errors = [0.25, 0.25, 0]
#        self.assertEqual((means, errors),
#                analyst_utils.collated_standard_error_of_mean(self.collated_data))
#
#    def test_collate_scale_noadd(self):
#        means = [3, 1, 0]
#        errors = [0.5, 0.5, 0]
#        self.assertEqual((means, errors),
#                analyst_utils.collated_standard_error_of_mean(self.collated_data,
#                    scale_by=2))
#
#    def test_collate_scale_add(self):
#        means = [4, 2, 1]
#        errors = [0.5, 0.5, 0]
#        self.assertEqual((means, errors),
#                analyst_utils.collated_standard_error_of_mean(self.collated_data,
#                    scale_by=2, add=1))


if '__main__' == __name__:
    unittest.main()
