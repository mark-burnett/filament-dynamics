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

from actin_dynamics.simulation.transitions.cooperative_hydrolysis import *

from actin_dynamics.simulation.strand_factories.strands.single_strand import Strand

from tests.mocks.concentrations import MockConcentration


class CooperativeHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.strand = Strand([1, 2, 3, 1, 2, 3, 1])
        self.normal_one = CooperativeHydrolysis(old_state=1,
                pointed_neighbor=3, rate=3, cooperativity=2,
                new_state=2, number=1)
        self.normal_two = CooperativeHydrolysis(old_state=2,
                pointed_neighbor=1, rate=2, cooperativity=3,
                new_state=3, number=1)
        self.normal_three = CooperativeHydrolysis(old_state=1,
                pointed_neighbor=2, rate=4, cooperativity=3,
                new_state=2, number=1)

        self.missing = CooperativeHydrolysis(old_state=4,
                pointed_neighbor=5, rate=7, cooperativity=1.5,
                new_state=8, number=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R([self.strand],   None), [15])
        self.assertEqual(self.normal_two.R([self.strand],   None), [12])
        self.assertEqual(self.normal_three.R([self.strand], None), [12])

    def test_missing_rates(self):
        self.assertEqual(self.missing.R([self.strand], None), [0])

    def test_perform_normal_boundary(self):
        self.normal_one.perform(None, [self.strand], None, 0, 0)
        self.assertEqual(self.strand.states, [1, 2, 3, 2, 2, 3, 1])
        self.assertEqual(self.normal_one.R([self.strand], None), [9])
        self.assertEqual(self.normal_two.R([self.strand], None), [10])

        self.normal_one.perform(None, [self.strand], None, 0, 0)
        self.assertEqual(self.strand.states, [1, 2, 3, 2, 2, 3, 2])
        self.assertEqual(self.normal_one.R([self.strand], None), [3])
        self.assertEqual(self.normal_two.R([self.strand], None), [12])

    def test_perform_normal_random(self):
        self.normal_one.perform(None, [self.strand], None, 0, 14)
        self.assertEqual(self.strand.states, [2, 2, 3, 1, 2, 3, 1])
        self.assertEqual(self.normal_one.R([self.strand], None), [12])
        self.assertEqual(self.normal_two.R([self.strand], None), [10])

    def test_perform_missing(self):
        self.assertRaises(IndexError, self.missing.perform,
                          None, [self.strand], None, 0, 0)


class CooperativeHydrolysisWithByproductTest(unittest.TestCase):
    def test_notice(self):
        # XXX Write some tests for this, and expand the above tests for multi filament.
        self.assertFalse(True)
#    def setUp(self):
#        self.strand = Strand([1, 2, 3, 1, 2, 3, 1])
#        self.concentrations = defaultdict(MockConcentration)
#
#        self.normal_one = CooperativeHydrolysisWithByproduct(old_state=1,
#                pointed_neighbor=3, rate=3, cooperativity=2,
#                new_state=2, byproduct=11, number=1)
#        self.normal_two = CooperativeHydrolysisWithByproduct(old_state=2,
#                pointed_neighbor=1, rate=2, cooperativity=3,
#                new_state=3, byproduct=12, number=1)
#        self.normal_three = CooperativeHydrolysisWithByproduct(old_state=1,
#                pointed_neighbor=2, rate=4, cooperativity=3,
#                new_state=2, byproduct=13, number=1)
#
#        self.missing = CooperativeHydrolysisWithByproduct(old_state=4,
#                pointed_neighbor=5, rate=7, cooperativity=1.5,
#                new_state=8, byproduct=14, number=1)
#
#    def test_normal_rates(self):
#        self.assertEqual(self.normal_one.R(self.strand,   None), 15)
#        self.assertEqual(self.normal_two.R(self.strand,   None), 12)
#        self.assertEqual(self.normal_three.R(self.strand, None), 12)
#
#    def test_missing_rates(self):
#        self.assertEqual(self.missing.R(self.strand, None), 0)
#
#    def test_perform_normal_boundary(self):
#        self.normal_one.perform(None, self.strand, self.concentrations, 0)
#        self.assertEqual(self.strand.states, [1, 2, 3, 2, 2, 3, 1])
#        self.assertEqual(self.normal_one.R(self.strand, None), 9)
#        self.assertEqual(self.normal_two.R(self.strand, None), 10)
#        self.assertEqual(self.concentrations[11].count, 1)
#
#        self.normal_one.perform(None, self.strand, self.concentrations, 0)
#        self.assertEqual(self.strand.states, [1, 2, 3, 2, 2, 3, 2])
#        self.assertEqual(self.normal_one.R(self.strand, None), 3)
#        self.assertEqual(self.normal_two.R(self.strand, None), 12)
#        self.assertEqual(self.concentrations[11].count, 2)
#
#    def test_perform_normal_random(self):
#        self.normal_one.perform(None, self.strand, self.concentrations, 14)
#        self.assertEqual(self.strand.states, [2, 2, 3, 1, 2, 3, 1])
#        self.assertEqual(self.normal_one.R(self.strand, None), 12)
#        self.assertEqual(self.normal_two.R(self.strand, None), 10)
#        self.assertEqual(self.concentrations[11].count, 1)
#
#    def test_perform_missing(self):
#        self.assertRaises(IndexError, self.missing.perform,
#                          None, self.strand, self.concentrations, 0)
#        self.assertEqual(self.concentrations[14].count, 0)


if '__main__' == __name__:
    unittest.main()
