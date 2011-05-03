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

from actin_dynamics.primitives.transitions.cooperative_hydrolysis import *

from actin_dynamics.species.single_strand_filaments import Filament

from unit_tests.mocks.concentrations import MockConcentration


class CooperativeHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.strand = Filament(['a', 'b', 'c', 'a', 'b', 'c', 'a'])
        self.normal_one = CooperativeHydrolysis(old_species='a',
                rate=3, new_species='b', c=2)
        self.normal_two = CooperativeHydrolysis(old_species='b',
                rate=2, new_species='c', a=3)
        self.normal_three = CooperativeHydrolysis(old_species='a',
                rate=4, new_species='b', b=3)

        self.missing = CooperativeHydrolysis(old_species='d',
                rate=7, new_species=8, e=1.5)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R([self.strand],   None), 15)
        self.assertEqual(self.normal_two.R([self.strand],   None), 12)
        self.assertEqual(self.normal_three.R([self.strand], None), 12)

    def test_missing_rates(self):
        self.assertEqual(self.missing.R([self.strand], None), 0)

    def test_perform_normal_boundary(self):
        self.test_normal_rates()
        self.normal_one.perform(None, [self.strand], None, 10)
        self.assertEqual(list(self.strand), ['a', 'b', 'c', 'b', 'b', 'c', 'a'])
        self.assertEqual(self.normal_one.R([self.strand], None), 9)
        self.assertEqual(self.normal_two.R([self.strand], None), 10)

        self.normal_one.perform(None, [self.strand], None, 8)
        self.assertEqual(list(self.strand), ['a', 'b', 'c', 'b', 'b', 'c', 'b'])
        self.assertEqual(self.normal_one.R([self.strand], None), 3)
        self.assertEqual(self.normal_two.R([self.strand], None), 12)

    def test_perform_normal_random(self):
        self.test_normal_rates()
        self.normal_one.R([self.strand], None)
        self.normal_one.perform(None, [self.strand], None, 0)
        self.assertEqual(list(self.strand), ['b', 'b', 'c', 'a', 'b', 'c', 'a'])
        self.assertEqual(self.normal_one.R([self.strand], None), 12)
        self.assertEqual(self.normal_two.R([self.strand], None), 10)

    def test_perform_missing(self):
        self.test_missing_rates()
        self.assertRaises(IndexError, self.missing.perform,
                          None, [self.strand], None, 0)



if '__main__' == __name__:
    unittest.main()
