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
import os.path

from actin_dynamics.primitives.file_readers import dat_files
from actin_dynamics.numerical import workalike

class FixedConcentrationTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'sample_data.dat'

        dirname, this_filename = os.path.split(__file__)
        self.base_directory = dirname

        self.xmin = 0
        self.xmax = 600
        self.sample_period = 10

        self.dr = dat_files.DatReader(filename=self.filename,
                                      base_directory=self.base_directory,
                                      interpolate_data=True,
                                      xmin=self.xmin, xmax=self.xmax,
                                      sample_period=self.sample_period)

    def test_interpolation_times(self):
        results = self.dr.run()

        expected_times = workalike.arange(self.xmin, self.xmax, self.sample_period)
        self.assertEqual(expected_times, results[0])

    def test_interpolation_increasing(self):
        # NOTE This test may fail with small sample periods, because the sample
        # data has fluctuations
        results = self.dr.run()

        last_value = 0
        for v in results[1]:
            self.assertTrue(v >= last_value, (v, last_value))
            last_value = v

    def test_interpolation_positive(self):
        results = self.dr.run()

        self.assertTrue(results[1][0] >= 0)

        for v in results[1][1:]:
            self.assertTrue(v > 0)


if '__main__' == __name__:
    unittest.main()
