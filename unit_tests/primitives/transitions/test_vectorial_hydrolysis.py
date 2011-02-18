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

from actin_dynamics.primitives.transitions.vectorial_hydrolysis import *
from actin_dynamics.primitives.filaments.single_strand_filaments import Filament

from unit_tests.mocks.concentrations import MockConcentration


class VectorialHydrolysisSingleFilamentTest(unittest.TestCase):
    def setUp(self):
        self.filament = Filament([1, 2, 3, 1, 2, 3, 1])

        self.normal_one = VectorialHydrolysis(old_state=1, pointed_neighbor=3,
                                              new_state=2, rate=3)
        self.normal_two = VectorialHydrolysis(old_state=2, pointed_neighbor=1,
                                              new_state=3, rate=2)
        self.missing    = VectorialHydrolysis(old_state=1, pointed_neighbor=2,
                                              new_state=7, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R([self.filament], None), [6])
        self.assertEqual(self.normal_two.R([self.filament], None), [4])

    def test_missing_rates(self):
        self.assertEqual(self.missing.R([self.filament], None), [0])

    def test_perform_normal(self):
        self.normal_one.perform(None, [self.filament], None, 0, 4)
        self.assertEqual(self.normal_one.R([self.filament], None), [3])
        self.assertEqual(self.normal_two.R([self.filament], None), [4])

        self.normal_two.perform(None, [self.filament], None, 0, 1)
        self.assertEqual(self.normal_one.R([self.filament], None), [3])
        self.assertEqual(self.normal_two.R([self.filament], None), [2])

    def test_perform_missing(self):
        self.assertRaises(IndexError, self.missing.perform,
                          None, [self.filament], None, 0, 0)


class VectorialHydrolysisMultipleFilamentTest(unittest.TestCase):
    def setUp(self):
        self.filaments = [Filament([1, 2, 3, 1, 2, 3, 1]),
                          Filament([2, 3, 1, 2, 3, 1, 2]),
                          Filament([3, 2, 1, 3, 2, 1, 3])]

        self.normal_one = VectorialHydrolysis(old_state=1, pointed_neighbor=3,
                                              new_state=2, rate=3)
        self.normal_two = VectorialHydrolysis(old_state=2, pointed_neighbor=1,
                                              new_state=3, rate=2)
        self.missing    = VectorialHydrolysis(old_state=1, pointed_neighbor=2,
                                              new_state=7, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R(self.filaments, None), [6, 6, 0])
        self.assertEqual(self.normal_two.R(self.filaments, None), [4, 4, 0])

    def test_missing_rates(self):
        self.assertEqual(self.missing.R(self.filaments, None), [0, 0, 2])

    def test_perform_normal(self):
        self.normal_one.perform(None, self.filaments, None, 0, 4)
        self.assertEqual(self.normal_one.R(self.filaments, None), [3, 6, 0])
        self.assertEqual(self.normal_two.R(self.filaments, None), [4, 4, 0])

        self.normal_two.perform(None, self.filaments, None, 0, 1)
        self.assertEqual(self.normal_one.R(self.filaments, None), [3, 6, 0])
        self.assertEqual(self.normal_two.R(self.filaments, None), [2, 4, 0])

        self.normal_one.perform(None, self.filaments, None, 1, 0)
        self.assertEqual(self.normal_one.R(self.filaments, None), [3, 3, 0])
        self.assertEqual(self.normal_two.R(self.filaments, None), [2, 2, 0])

        self.missing.perform(None, self.filaments, None, 2, 0)
        self.assertEqual(self.normal_one.R(self.filaments, None), [3, 3, 0])
        self.assertEqual(self.normal_two.R(self.filaments, None), [2, 2, 0])
        self.assertEqual(self.missing.R(self.filaments, None),    [0, 0, 1])

    def test_perform_missing(self):
        self.assertRaises(IndexError, self.missing.perform,
                          None, self.filaments, None, 0, 0)

        self.assertRaises(IndexError, self.missing.perform,
                          None, self.filaments, None, 1, 0)


class VectorialHydrolysisWithByproductSingleFilamentTest(unittest.TestCase):
    def setUp(self):
        self.filament = Filament([1, 2, 3, 1, 2, 3, 1])
        self.concentrations = defaultdict(MockConcentration)

        self.normal_one = VectorialHydrolysisWithByproduct(old_state=1,
                                                           pointed_neighbor=3,
                                                           new_state=2, rate=3,
                                                           byproduct=11)
        self.normal_two = VectorialHydrolysisWithByproduct(old_state=2,
                                                           pointed_neighbor=1,
                                                           new_state=3, rate=2,
                                                           byproduct=12)
        self.missing    = VectorialHydrolysisWithByproduct(old_state=1,
                                                           pointed_neighbor=2,
                                                           new_state=7, rate=1,
                                                           byproduct=17)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R([self.filament], None), [6])
        self.assertEqual(self.normal_two.R([self.filament], None), [4])

    def test_missing_rates(self):
        self.assertEqual(self.missing.R([self.filament], None), [0])

    def test_perform_normal(self):
        self.normal_one.perform(None, [self.filament], self.concentrations, 0, 4)
        self.assertEqual(self.normal_one.R([self.filament], None), [3])
        self.assertEqual(self.normal_two.R([self.filament], None), [4])
        self.assertEqual(self.concentrations[11].count, 1)

        self.normal_two.perform(None, [self.filament], self.concentrations, 0, 1)
        self.assertEqual(self.normal_one.R([self.filament], None), [3])
        self.assertEqual(self.normal_two.R([self.filament], None), [2])
        self.assertEqual(self.concentrations[12].count, 1)

    def test_perform_missing(self):
        self.assertRaises(IndexError, self.missing.perform,
                          None, [self.filament], None, 0, 0)
        self.assertEqual(self.concentrations[17].count, 0)


if '__main__' == __name__:
    unittest.main()
