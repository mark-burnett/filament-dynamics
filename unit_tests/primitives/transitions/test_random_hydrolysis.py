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

from actin_dynamics.primitives.transitions.random_hydrolysis import *
from actin_dynamics.state.single_strand_filaments import Filament

from unit_tests.mocks.concentrations import MockConcentration


class RandomHydrolysisSingleFilamentTest(unittest.TestCase):
    def setUp(self):
        self.filament = Filament([1, 2, 3, 1, 2, 3, 1])
        self.transition_one  = RandomHydrolysis(old_state=1, new_state=2,
                                                rate=3)
        self.transition_two  = RandomHydrolysis(old_state=2, new_state=3,
                                                rate=2)
        self.transition_four = RandomHydrolysis(old_state=4, new_state=5,
                                                rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.transition_one.R([self.filament], None), 9)
        self.assertEqual(self.transition_two.R([self.filament], None), 4)

    def test_missing_rates(self):
        self.assertEqual(self.transition_four.R([self.filament], None), 0)

    def test_perform_normal(self):
        self.test_normal_rates()
        self.transition_one.perform(None, [self.filament], None, 0)
        self.assertEqual(self.transition_one.R([self.filament], None), 6)
        self.assertEqual(self.transition_two.R([self.filament], None), 6)

        self.transition_one.perform(None, [self.filament], None, 5.9)
        self.assertEqual(self.transition_one.R([self.filament], None), 3)
        self.assertEqual(self.transition_two.R([self.filament], None), 8)

        self.transition_two.perform(None, [self.filament], None, 1)
        self.assertEqual(self.transition_two.R([self.filament], None), 6)

    def test_perform_missing(self):
        self.test_missing_rates()
        self.assertRaises(IndexError, self.transition_four.perform,
                          None, [self.filament], None, 0)


class RandomHydrolysisMultipleFilamentTest(unittest.TestCase):
    def setUp(self):
        self.filaments = [Filament([1, 2, 3, 1, 2, 3, 1]),
                          Filament([2, 3, 1, 2, 3, 1, 2]),
                          Filament([3, 2, 1, 4, 2, 1, 3])]
        self.transition_one  = RandomHydrolysis(old_state=1, new_state=2,
                                                rate=3)
        self.transition_two  = RandomHydrolysis(old_state=2, new_state=3,
                                                rate=2)
        self.transition_four = RandomHydrolysis(old_state=4, new_state=5,
                                                rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.transition_one.R(self.filaments, None), 21)
        self.assertEqual(self.transition_two.R(self.filaments, None), 14)

    def test_missing_rates(self):
        self.assertEqual(self.transition_four.R(self.filaments, None), 1)

    def test_perform_normal(self):
        self.test_normal_rates()
        self.transition_one.perform(None, self.filaments, None, 0)
        self.assertEqual(self.transition_one.R(self.filaments, None), 18)
        self.assertEqual(self.transition_two.R(self.filaments, None), 16)

        self.transition_one.perform(None, self.filaments, None, 0)
        self.assertEqual(self.transition_one.R(self.filaments, None), 15)
        self.assertEqual(self.transition_two.R(self.filaments, None), 18)

        self.transition_one.perform(None, self.filaments, None, 0)
        self.assertEqual(self.transition_one.R(self.filaments, None), 12)
        self.assertEqual(self.transition_two.R(self.filaments, None), 20)


class RandomHydrolysisWithByproductSingleFilamentTest(unittest.TestCase):
    def setUp(self):
        self.filament = Filament([1, 2, 3, 1, 2, 3, 1])
        self.concentrations = defaultdict(MockConcentration)
        self.transition_one = RandomHydrolysisWithByproduct(old_state=1,
                new_state=2, byproduct=11, rate=3)
        self.transition_two = RandomHydrolysisWithByproduct(old_state=2,
                new_state=3, byproduct=12, rate=2)
        self.transition_four = RandomHydrolysisWithByproduct(old_state=4,
                new_state=5, byproduct=14, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.transition_one.R([self.filament], None), 9)
        self.assertEqual(self.transition_two.R([self.filament], None), 4)

    def test_missing_rates(self):
        self.assertEqual(self.transition_four.R([self.filament], None), 0)

    def test_perform_normal(self):
        self.test_normal_rates()
        self.transition_one.perform(None, [self.filament], self.concentrations, 0)
        self.assertEqual(self.transition_one.R([self.filament], None), 6)
        self.assertEqual(self.transition_two.R([self.filament], None), 6)
        self.assertEqual(self.concentrations[11].count, 1)

        self.transition_one.perform(None, [self.filament], self.concentrations, 5.9)
        self.assertEqual(self.transition_one.R([self.filament],
                         self.concentrations), 3)
        self.assertEqual(self.transition_two.R([self.filament], None), 8)
        self.assertEqual(self.concentrations[11].count, 2)

        self.transition_two.perform(None, [self.filament], self.concentrations, 1)
        self.assertEqual(self.transition_two.R([self.filament], None), 6)
        self.assertEqual(self.concentrations[11].count, 2)
        self.assertEqual(self.concentrations[12].count, 1)

    def test_perform_missing(self):
        self.test_missing_rates()
        self.assertRaises(IndexError, self.transition_four.perform,
                          None, [self.filament], self.concentrations, 0)
        self.assertEqual(self.concentrations[14].count, 0)


if '__main__' == __name__:
    unittest.main()
