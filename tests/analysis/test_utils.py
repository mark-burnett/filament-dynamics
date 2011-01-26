#    Copyright (C) 2010 Mark Burnett
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

import itertools

import numpy

from actin_dynamics.analysis import utils


def expected_result(measurement, factor):
    times = measurement[0]
    rest  = numpy.array(measurement[1:])

    partial_result = factor * rest

    result = [times]
    for row in partial_result:
        result.append(list(row))

    return result


class TestScaleMeasurement(unittest.TestCase):
    def setUp(self):
        self.factor = 0.5

        self.small_measurement = [
                range(10),
                [4, 3, 5, 2, 1, 7, 8, 3, 2, 1]]

        self.medium_measurement = [
                range(10),
                [4, 3, 5, 2, 1, 7, 8, 3, 2, 1],
                [2, 1, 3, 1, 0, 4, 7, 1, 1, 0]]

        self.large_measurement = [
                range(10),
                [4, 3, 5, 2, 1, 7, 8, 3, 2, 1],
                [3, 2, 2, 1, 0, 5, 5, 1, 1, 0],
                [6, 4, 6, 5, 2, 8, 10, 6, 5, 3]]

        self.transformed_small = expected_result(self.small_measurement,
                                                 self.factor)
        self.transformed_medium = expected_result(self.medium_measurement,
                                                 self.factor)
        self.transformed_large = expected_result(self.large_measurement,
                                                 self.factor)

    def assert_measurement_equal(self, m1, m2):
        for r1, r2 in itertools.izip(m1, m2):
            self.assertEqual(r1, r2)

    def test_scale_measurement(self):
        self.assert_measurement_equal(self.transformed_small,
                utils.scale_measurement(self.small_measurement, self.factor))

        self.assert_measurement_equal(self.transformed_medium,
                utils.scale_measurement(self.medium_measurement, self.factor))

        self.assert_measurement_equal(self.transformed_large,
                utils.scale_measurement(self.large_measurement, self.factor))

    def test_scaled_sum(self):
        self.assertEqual(sum(self.small_measurement[1]) * self.factor,
                         sum(self.transformed_small[1]))

        self.assertEqual(sum(self.medium_measurement[1]) * self.factor,
                         sum(self.transformed_medium[1]))

        self.assertEqual(sum(self.large_measurement[1]) * self.factor,
                         sum(self.transformed_large[1]))
