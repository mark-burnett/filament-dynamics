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

from collections import defaultdict

from actin_dynamics.primitives.transitions.polymerization import BarbedPolymerization

from actin_dynamics.state.single_strand_filaments import Filament

from unit_tests.mocks.concentrations import MockConcentration

class BarbedPolymerizationSingleFilament(unittest.TestCase):
    def setUp(self):
        self.filament = Filament([None, None, None])

        self.concentrations = defaultdict(MockConcentration)
        self.concentrations[1] = MockConcentration(value=3)
        self.concentrations[2] = MockConcentration(value=7)

        self.poly_one = BarbedPolymerization(state=1, rate=1)
        self.poly_two = BarbedPolymerization(state=2, rate=2)

    def test_rates(self):
        self.assertEqual(self.poly_one.R([self.filament], self.concentrations), 3)
        self.assertEqual(self.poly_two.R([self.filament], self.concentrations), 14)

    def test_normal_perform(self):
        self.test_rates()
        self.poly_one.perform(None, [self.filament], self.concentrations, 0)
        self.assertEqual(list(self.filament), [None, None, None, 1])

        self.poly_two.perform(None, [self.filament], self.concentrations, 0)
        self.assertEqual(list(self.filament), [None, None, None, 1, 2])

        self.poly_one.perform(None, [self.filament], self.concentrations, 0)
        self.assertEqual(list(self.filament), [None, None, None, 1, 2, 1])

        # Validate rates after some transitions.
        self.test_rates()

#class PointedPolymerization(unittest.TestCase):
#    def test_write_me_please(self):
#        self.assertTrue(False)

if '__main__' == __name__:
    unittest.main()
