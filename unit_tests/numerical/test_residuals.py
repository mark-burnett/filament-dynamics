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

from actin_dynamics.numerical import residuals

class ResidualsTest(unittest.TestCase):
    def setUp(self):
        self.length   = 10
        self.epsilon  = 0.1

        self.a_values = range(self.length)
        self.b_values = [self.epsilon + av for av in self.a_values]

        self.a = (None, self.a_values, None)
        self.b = (None, self.b_values, None)

    def test_naked_chi_squared(self):
        expected_result = self.epsilon**2
        self.assertAlmostEqual(expected_result,
                               residuals.naked_chi_squared(self.a, self.b))


if '__main__' == __name__:
    unittest.main()

