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

from actin_dynamics.numerical import interpolation

class TestLinearProject(unittest.TestCase):
    def test_linear_project(self):
        test_data = [({'x1': 2, 'x2': 3, 'x3': 5,
                       'y1': 6, 'y2': 7},      9),
                     ({'x1': 2, 'x2': 3, 'x3': 1,
                       'y1': 6, 'y2': 7},      5),
                     ({'x1': 2, 'x2': 3, 'x3': 5,
                       'y1': 1, 'y2': 5},     13),
                     ({'x1': 2, 'x2': 3, 'x3': 1,
                       'y1': 1, 'y2': 5},     -3),
                     ({'x1': 1, 'x2': 3, 'x3': 2,
                       'y1': 1, 'y2': 5},      3)]

        for kwargs, result in test_data:
            self.assertEqual(result, interpolation.linear_project(**kwargs))

class TestInterp1D(unittest.TestCase):
    def setUp(self):
        self.x_mesh = [2*i for i in xrange(10)]
        self.y_mesh = [4*i for i in xrange(10)]

        self.linterp = interpolation.interp1d(self.x_mesh, self.y_mesh)

    def test_middle(self):
        test_data = [(1, 2),
                     (2, 4)]

        for x, y in test_data:
            self.assertEqual(y, self.linterp(x))

    def test_start(self):
        self.assertRaises(IndexError, self.linterp, 0)

    def test_before_start(self):
        self.assertRaises(IndexError, self.linterp, -1)

    def test_end(self):
        self.assertEqual(self.y_mesh[-1], self.linterp(self.x_mesh[-1]))
        self.assertEqual(34, self.linterp(17))

    def test_after_end(self):
        self.assertRaises(IndexError, self.linterp, self.x_mesh[-1] + 1)

class TestLineaerResample(unittest.TestCase):
    def setUp(self):
        self.x_mesh = [2*i for i in xrange(10)]
        self.y_mesh = [3, 7, 5, 1, 3, 1, 7, 9, 11, 5]
        self.measurement = (self.x_mesh, self.y_mesh)

    def test_middle(self):
        new_x = [2*i + 1 for i in xrange(9)]
        new_y = map(float, [5, 6, 3, 2, 2, 4, 8, 10, 8])

        results = (new_x, new_y)

        self.assertEqual(results,
                interpolation.linear_resample(self.measurement, new_x))

    def test_before_start(self):
        new_x = range(-3, 0) + range(0, 3)
        new_y = [-3.0, -1.0, 1.0, 3.0, 5.0, 7.0]

        results = (new_x, new_y)

        self.assertEqual(results,
                interpolation.linear_resample(self.measurement, new_x))

    def test_after_end(self):
        new_x = [15 + i for i in xrange(7)]
        new_y = [10.0, 11.0, 8.0, 5.0, 2.0, -1.0, -4.0]

        results = (new_x, new_y)

        self.assertEqual(results,
                interpolation.linear_resample(self.measurement, new_x))


if '__main__' == __name__:
    unittest.main()
