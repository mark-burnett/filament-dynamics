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

import math

from actin_dynamics.primitives.analysts import derivative

from actin_dynamics import database


class KeyedDerivativeTest(unittest.TestCase):
    def setUp(self):
        self.data = {'my name': [
                        {'A': [[0, 0.5, 1, 1.5, 2], [2, 1, 0, 3, 4]],
                         'B': [[0, 0.25, 0.5, 0.75, 1], [2, 1, 0, 3, 4]]},
                        {'C': [[0, 2, 4], [2, 3, 4]]}]}
        self.expected_result = {'A': ([0, 0.5, 1, 1.5], [-2, -2, 6, 2]),
                                'B': ([0, 0.25, 0.5, 0.75], [-4, -4, 12, 4]),
                                'C': ([0, 2], [0.5, 0.5])}

    def test_analyze(self):
        analyst = derivative.KeyedDerivative(
                source_name='my name', source_type='observation',
                label='test label')
        analysis = analyst.analyze(self.data, None)
        self.assertTrue(isinstance(analysis, database.Analysis))
        self.assertEqual(self.expected_result, analysis.value)


if '__main__' == __name__:
    unittest.main()
