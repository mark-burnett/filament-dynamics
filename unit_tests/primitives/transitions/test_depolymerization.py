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

from unit_tests.mocks.concentrations import MockConcentration
from actin_dynamics.species.single_strand_filaments import Filament

from actin_dynamics.primitives.transitions.depolymerization import BarbedDepolymerization

class BarbedDepolymerizationSingleFilament(unittest.TestCase):
    def setUp(self):
        self.filament = Filament([None, 1, 2, 1])
        self.concentrations = defaultdict(MockConcentration)

        self.depoly_one = BarbedDepolymerization(species=1, rate=1)
        self.depoly_two = BarbedDepolymerization(species=2, rate=2)

    def test_rates(self):
        self.assertEqual(self.depoly_one.R([self.filament], None), 1)
        self.assertEqual(self.depoly_two.R([self.filament], None), 0)

    def test_normal_perform(self):
        self.test_rates()
        self.depoly_one.perform(None, [self.filament], self.concentrations, 0)
        self.assertEqual(list(self.filament), [None, 1, 2])
        self.assertEqual(self.depoly_one.R([self.filament], None), 0)
        self.assertEqual(self.depoly_two.R([self.filament], None), 2)

        self.depoly_two.perform(None, [self.filament], self.concentrations, 0)
        self.assertEqual(list(self.filament), [None, 1])
        self.assertEqual(self.depoly_one.R([self.filament], None), 1)
        self.assertEqual(self.depoly_two.R([self.filament], None), 0)

        self.depoly_one.perform(None, [self.filament], self.concentrations, 0)
        self.assertEqual(list(self.filament), [None])
        self.assertEqual(self.depoly_one.R([self.filament], None), 0)
        self.assertEqual(self.depoly_two.R([self.filament], None), 0)

if '__main__' == __name__:
    unittest.main()
