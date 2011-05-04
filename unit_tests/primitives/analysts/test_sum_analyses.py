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

import math
import unittest

from actin_dynamics.primitives.analysts import sum_analyses

from actin_dynamics import database

class SumAnalysesTest(unittest.TestCase):
    def setUp(self):
        A_error = [0.5,  0.25, 0.5]
        B_error = [0.25, 0.5,  0.5]
        A_analysis = database.Analysis(value=(range(3), [1, 3, 2], A_error))
        B_analysis = database.Analysis(value=(range(3), [2, 1, 2], B_error))
        self.analyses = {'A': A_analysis, 'B': B_analysis}

        values = [8, 9, 10]
        errors = [math.sqrt((2 * a)**2 + (3 * b)**2)
                  for a, b in zip(A_error, B_error)]
        self.expected_result = (range(3), values, errors)

    def test_analyze(self):
        analyst = sum_analyses.SumAnalyses(label='test label', A=2, B=3)
        analysis = analyst.analyze(None, self.analyses)
        self.assertTrue(isinstance(analysis, database.Analysis))
        self.assertEqual(self.expected_result, analysis.value)


if '__main__' == __name__:
    unittest.main()
