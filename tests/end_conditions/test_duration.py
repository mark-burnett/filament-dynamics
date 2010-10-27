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

from actin_dynamics.simulation import end_conditions

class DurationTest(unittest.TestCase):
    def test_normal_duration(self):
        d = end_conditions.Duration(17)
        self.assertFalse(d(0,  None, None))
        self.assertFalse(d(5,  None, None))
        self.assertFalse(d(16, None, None))
        self.assertFalse(d(17, None, None))
        self.assertTrue(d( 18, None, None))
        self.assertTrue(d(131, None, None))
    
    def test_zero_duration(self):
        self.assertRaises(ValueError, end_conditions.Duration, 0)

    def test_negative_duration(self):
        self.assertRaises(ValueError, end_conditions.Duration, -1)
        self.assertRaises(ValueError, end_conditions.Duration, -17)

class RandomDurationTest(unittest.TestCase):
    def test_normal_duration(self):
        durations = [20, 6, 107, 85.0]
        for d in durations:
            rd = end_conditions.RandomDuration(d)
            rd.reset()
            self.assertTrue(rd.duration < d)

            cd = rd.duration
            self.assertFalse(rd(cd - 1, None, None))
            self.assertTrue( rd(cd + 1, None, None))
            self.assertFalse(rd(float(cd)/2, None, None))
            self.assertTrue( rd(float(cd)*2, None, None))

            self.assertTrue(rd(d, None, None))

    def test_zero_duration(self):
        self.assertRaises(ValueError, end_conditions.RandomDuration, 0)

    def test_negative_duration(self):
        self.assertRaises(ValueError, end_conditions.RandomDuration, -1)
        self.assertRaises(ValueError, end_conditions.RandomDuration, -17)

if '__main__' == __name__:
    unittest.main()
