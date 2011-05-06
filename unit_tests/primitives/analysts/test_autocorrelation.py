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

from actin_dynamics.primitives.analysts import autocorrelation

from actin_dynamics import database

class AutocorrelationTest(unittest.TestCase):
    def setUp(self):
        a_times  = [0.3, 0.4, 0.5, 0.6, 0.7]
        a_values = [1.5, 2.0, 1.0, 0.0, 0.5]
        b_times  = [0.0, 0.1, 0.2, 0.3, 0.4]
        b_values = [0.5, 1.5, 1.5, 1.0, 0.5]
        c_times  = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        c_values = [1.0, 2.0, 1.5, 0.5, 0.5, 1.0]
        self.data = {'my name':
                     {'A': (a_times, a_values),
                      'B': (b_times, b_values),
                      'C': (c_times, c_values)}}

    def test_analyze_analyses(self):
        analyst = autocorrelation.Autocorrelation(
                source_name='my name', source_type='analyses',
                label='test label')
        analysis = analyst.analyze(None, self.data)
        self.assertTrue(isinstance(analysis, database.Analysis))
        t0 = analysis.value[0][0]
        v0 = analysis.value[1][0]
        e0 = analysis.value[2][0]
        self.assertEqual(t0, 0)
        self.assertAlmostEqual(1, v0)
        self.assertTrue(1 + 2*e0 > v0, 'v0 = %s, e0 = %s' % (v0, e0))
        self.assertTrue(1 - 2*e0 < v0, 'v0 = %s, e0 = %s' % (v0, e0))

    def test_better(self):
        self.assertTrue(False, 'seriously, this needs attention')


if '__main__' == __name__:
    unittest.main()
