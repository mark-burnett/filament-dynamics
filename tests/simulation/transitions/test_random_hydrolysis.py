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

from actin_dynamics.simulation.transitions.random_hydrolysis import *
from actin_dynamics.simulation.strands import Strand

from tests.mocks.concentrations import MockConcentration


class RandomHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.strand = Strand([1, 2, 3, 1, 2, 3, 1])
        self.transition_one = RandomHydrolysis(old_state=1, new_state=2, rate=3)
        self.transition_two = RandomHydrolysis(old_state=2, new_state=3, rate=2)
        self.transition_four = RandomHydrolysis(old_state=4, new_state=5, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.transition_one.R(self.strand, None), 9)
        self.assertEqual(self.transition_two.R(self.strand, None), 4)

    def test_missing_rates(self):
        self.assertEqual(self.transition_four.R(self.strand, None), 0)

    def test_perform_normal(self):
        self.transition_one.perform(None, self.strand, None, 0)
        self.assertEqual(self.transition_one.R(self.strand, None), 6)
        self.assertEqual(self.transition_two.R(self.strand, None), 6)

        self.transition_one.perform(None, self.strand, None, 5.9)
        self.assertEqual(self.transition_one.R(self.strand, None), 3)
        self.assertEqual(self.transition_two.R(self.strand, None), 8)

        self.transition_two.perform(None, self.strand, None, 1)
        self.assertEqual(self.transition_two.R(self.strand, None), 6)

    def test_perform_missing(self):
        self.assertRaises(IndexError, self.transition_four.perform,
                          None, self.strand, None, 0)


class RandomHydrolysisWithByproductTest(unittest.TestCase):
    def setUp(self):
        self.strand = Strand([1, 2, 3, 1, 2, 3, 1])
        self.concentrations = defaultdict(MockConcentration)

        self.transition_one = RandomHydrolysisWithByproduct(old_state=1,
                new_state=2, byproduct=11, rate=3)
        self.transition_two = RandomHydrolysisWithByproduct(old_state=2,
                new_state=3, byproduct=12, rate=2)
        self.transition_four = RandomHydrolysisWithByproduct(old_state=4,
                new_state=5, byproduct=14, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.transition_one.R(self.strand, None), 9)
        self.assertEqual(self.transition_two.R(self.strand, None), 4)

    def test_missing_rates(self):
        self.assertEqual(self.transition_four.R(self.strand, None), 0)

    def test_perform_normal(self):
        self.transition_one.perform(None, self.strand, self.concentrations, 0)
        self.assertEqual(self.transition_one.R(self.strand, None), 6)
        self.assertEqual(self.transition_two.R(self.strand, None), 6)
        self.assertEqual(self.concentrations[11].count, 1)

        self.transition_one.perform(None, self.strand, self.concentrations, 5.9)
        self.assertEqual(self.transition_one.R(self.strand, None), 3)
        self.assertEqual(self.transition_two.R(self.strand, None), 8)
        self.assertEqual(self.concentrations[11].count, 2)

        self.transition_two.perform(None, self.strand, self.concentrations, 1)
        self.assertEqual(self.transition_two.R(self.strand, None), 6)
        self.assertEqual(self.concentrations[11].count, 2)
        self.assertEqual(self.concentrations[12].count, 1)

    def test_perform_missing(self):
        self.assertRaises(IndexError, self.transition_four.perform,
                          None, self.strand, self.concentrations, 0)
        self.assertEqual(self.concentrations[14].count, 0)


if '__main__' == __name__:
    unittest.main()
