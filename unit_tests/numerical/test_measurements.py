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
import math

import numpy

from actin_dynamics.numerical import measurements


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
                measurements.scale(self.small_measurement, self.factor))

        self.assert_measurement_equal(self.transformed_medium,
                measurements.scale(self.medium_measurement, self.factor))

        self.assert_measurement_equal(self.transformed_large,
                measurements.scale(self.large_measurement, self.factor))

    def test_scaled_sum(self):
        self.assertEqual(sum(self.small_measurement[1]) * self.factor,
                         sum(self.transformed_small[1]))

        self.assertEqual(sum(self.medium_measurement[1]) * self.factor,
                         sum(self.transformed_medium[1]))

        self.assertEqual(sum(self.large_measurement[1]) * self.factor,
                         sum(self.transformed_large[1]))

class TestAddMeasurements(unittest.TestCase):
    def setUp(self):
        self.measurement_1 = [
                range(10),
                [4, 3, 5, 2, 1, 7, 8, 3, 2, 1],
                [2, 1, 3, 1, 0, 4, 7, 1, 1, 0]]

        self.measurement_2 = [
                range(10),
                [1, 3, 2, 7, 6, 8, 2, 1, 9, 3],
                [2, 1, 4, 4, 2, 3, 1, 1, 2, 3]]

    def test_double_measurement(self):
        expected_1 = [range(10),
                      [2*m for m in self.measurement_1[1]],
                      [math.sqrt(2*(m**2)) for m in self.measurement_1[2]]]

        result_1 = measurements.add([self.measurement_1, self.measurement_1])

        self.assertEqual(expected_1[0], result_1[0])
        self.assertEqual(expected_1[1], result_1[1])
        for e, r in zip(expected_1[2], result_1[2]):
            self.assertAlmostEqual(e, r)

        expected_2 = [range(10),
                      [2*m for m in self.measurement_2[1]],
                      [math.sqrt(2*(m**2)) for m in self.measurement_2[2]]]

        result_2 = measurements.add([self.measurement_2, self.measurement_2])

        self.assertEqual(expected_2[0], result_2[0])
        self.assertEqual(expected_2[1], result_2[1])
        for e, r in zip(expected_2[2], result_2[2]):
            self.assertAlmostEqual(e, r)

    def test_add_measurement(self):
        result = measurements.add([self.measurement_1, self.measurement_2])
        expected_values = [a + b for a, b in zip(self.measurement_1[1],
                                                 self.measurement_2[1])]
        expected_errors = [math.sqrt(a**2 + b**2)
                           for a, b in zip(self.measurement_1[2],
                                           self.measurement_2[2])]

        self.assertEqual(range(10), result[0])
        self.assertEqual(expected_values, result[1])
        self.assertEqual(expected_errors, result[2])
