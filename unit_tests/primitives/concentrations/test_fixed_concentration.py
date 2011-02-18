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

from actin_dynamics.primitives import concentrations

class FixedConcentrationTest(unittest.TestCase):
    def test_typical_FixedConcentration(self):
        values = [3.1, 0.0001, 7]
        for v in values:
            fc = concentrations.FixedConcentration(v)
            self.assertEqual(v, fc.value)

    def test_negative_FixedConcentration(self):
        self.assertRaises(ValueError, concentrations.FixedConcentration, -0.5)

    def test_ZeroConcentration(self):
        zc = concentrations.ZeroConcentration()
        self.assertEqual(0, zc.value)

if '__main__' == __name__:
    unittest.main()
