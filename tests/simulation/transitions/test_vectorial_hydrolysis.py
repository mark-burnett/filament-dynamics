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

from actin_dynamics.simulation.transitions.vectorial_hydrolysis import *
from actin_dynamics.simulation.strands import Strand

class MockConcentration(object):
    def __init__(self):
        self.count = 0

    def add_monomer(self):
        self.count += 1

    def remove_monomer(self):
        self.count -= 1


class VectorialHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.strand = Strand([1, 2, 3, 1, 2, 3, 1])

        self.normal_one = VectorialHydrolysis(old_state=1, pointed_neighbor=3,
                                              new_state=2, rate=3)
        self.normal_two = VectorialHydrolysis(old_state=2, pointed_neighbor=1,
                                              new_state=3, rate=2)
        self.missing    = VectorialHydrolysis(old_state=1, pointed_neighbor=2,
                                              new_state=7, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R(self.strand, None), 6)
        self.assertEqual(self.normal_two.R(self.strand, None), 4)

    def test_missing_rates(self):
        self.assertEqual(self.missing.R(self.strand, None), 0)

    def test_perform_normal(self):
        self.normal_one.perform(None, self.strand, None, 4)
        self.assertEqual(self.normal_one.R(self.strand, None), 3)
        self.assertEqual(self.normal_two.R(self.strand, None), 4)

        self.normal_two.perform(None, self.strand, None, 1)
        self.assertEqual(self.normal_one.R(self.strand, None), 3)
        self.assertEqual(self.normal_two.R(self.strand, None), 2)

    def test_perform_missing(self):
        self.assertRaises(IndexError, self.missing.perform,
                          None, self.strand, None, 0)

class VectorialHydrolysisWithByproductTest(unittest.TestCase):
    def setUp(self):
        self.strand = Strand([1, 2, 3, 1, 2, 3, 1])
        self.concentrations = defaultdict(MockConcentration)

        self.normal_one = VectorialHydrolysisWithByproduct(old_state=1,
                pointed_neighbor=3, new_state=2, byproduct=11, rate=3)
        self.normal_two = VectorialHydrolysisWithByproduct(old_state=2,
                pointed_neighbor=1, new_state=3, byproduct=12, rate=2)
        self.missing    = VectorialHydrolysisWithByproduct(old_state=1,
                pointed_neighbor=2, new_state=7, byproduct=17, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R(self.strand, None), 6)
        self.assertEqual(self.normal_two.R(self.strand, None), 4)

    def test_missing_rates(self):
        self.assertEqual(self.missing.R(self.strand, None), 0)

    def test_perform_normal(self):
        self.normal_one.perform(None, self.strand, self.concentrations, 4)
        self.assertEqual(self.normal_one.R(self.strand, None), 3)
        self.assertEqual(self.normal_two.R(self.strand, None), 4)
        self.assertEqual(self.concentrations[11].count, 1)

        self.normal_two.perform(None, self.strand, self.concentrations, 1)
        self.assertEqual(self.normal_one.R(self.strand, None), 3)
        self.assertEqual(self.normal_two.R(self.strand, None), 2)
        self.assertEqual(self.concentrations[12].count, 1)

    def test_perform_missing(self):
        self.assertRaises(IndexError, self.missing.perform,
                          None, self.strand, self.concentrations, 0)
        self.assertEqual(self.concentrations[17].count, 0)


if '__main__' == __name__:
    unittest.main()
