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

import numpy

from actin_dynamics.numerical import correlation


class AutocorrelationTest(unittest.TestCase):
    def setUp(self):
        self.a = [1, 2, 1, 0, 2, 1, 2, 0]

        self.expected_a = [1.0, -0.53113553113553114, -0.0085470085470085461,
                -0.34358974358974359, 0.38461538461538464, 0.50427350427350426,
                -0.89743589743589747, 0.23076923076923078]

    def test_autocorrelation(self):
        values = [1, 2, 1, 0, 2, 1, 2, 0]

        expected = [1.0, -0.53113553113553114, -0.0085470085470085461,
                -0.34358974358974359, 0.38461538461538464, 0.50427350427350426,
                -0.89743589743589747, 0.23076923076923078]

        result = list(correlation.autocorrelation(values))

        # Sanity checks
        self.assertAlmostEqual(1, result[0])
        for v in result[1:]:
            self.assertTrue(1 > v)

        # Actual equality check.
        self.assertEqual(expected, result)


if '__main__' == __name__:
    unittest.main()
