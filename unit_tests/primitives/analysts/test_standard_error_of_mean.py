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

from actin_dynamics.primitives.analysts import standard_error_of_mean

from actin_dynamics import database

class SEMTest(unittest.TestCase):
    def setUp(self):
        self.collated_data = [[2, 1, 1, 2], [1, 0, 0, 1], [0, 0]]

    def test_noscale_noadd(self):
        means = [1.5, 0.5, 0]
        errors = [0.25, 0.25, 0]
        self.assertEqual((means, errors),
                standard_error_of_mean._sem(self.collated_data))

    def test_scale_noadd(self):
        means = [3, 1, 0]
        errors = [0.5, 0.5, 0]
        self.assertEqual((means, errors),
                standard_error_of_mean._sem(self.collated_data, scale_by=2))

    def test_scale_add(self):
        means = [4, 2, 1]
        errors = [0.5, 0.5, 0]
        self.assertEqual((means, errors),
                standard_error_of_mean._sem(self.collated_data, scale_by=2, add=1))

class StandardErrorMeanTest(unittest.TestCase):
    def setUp(self):
        self.data = {'my name':
                     [{'A': [range(3), list(reversed(range(3)))],
                       'B': [range(2), list(reversed(range(2)))]},
                      {'C': [range(2), list(reversed(range(2)))],
                       'D': [range(3), list(reversed(range(3)))]}]}

        means = [1.5, 0.5, 0]
        errors = [0.25, 0.25, 0]
        self.expected_result = (range(3), means, errors)

    def test_analyze_analyses(self):
        analyst = standard_error_of_mean.StandardErrorMean(
                source_name='my name', source_type='analyses',
                label='test label')
        analysis = analyst.analyze(None, self.data)
        self.assertTrue(isinstance(analysis, database.Analysis))
        self.assertEqual(self.expected_result, analysis.value)

    def test_analyze_observations(self):
        analyst = standard_error_of_mean.StandardErrorMean(
                source_name='my name', source_type='observation',
                label='test label')
        analysis = analyst.analyze(self.data, None)
        self.assertTrue(isinstance(analysis, database.Analysis))
        self.assertEqual(self.expected_result, analysis.value)

    def test_analyze_raises(self):
        analyst = standard_error_of_mean.StandardErrorMean(
                source_name='my name', source_type='unknown',
                label='test label')
        self.assertRaises(RuntimeError, analyst.analyze, None, None)


if '__main__' == __name__:
    unittest.main()
