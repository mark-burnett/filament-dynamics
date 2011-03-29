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

from actin_dynamics.primitives.transitions.concentration_changes import *

from unit_tests.mocks.concentrations import MockConcentration

class ConcentrationChangeTest(unittest.TestCase):
    def setUp(self):
        self.concentrations = defaultdict(MockConcentration)

        self.concentrations[1] = MockConcentration(value=10)
        self.concentrations[2] = MockConcentration(value=20)

        self.normal_one = ConcentrationChange(old_state=1, new_state=2, rate=3)
        self.normal_two = ConcentrationChange(old_state=2, new_state=3, rate=2)

        self.missing = ConcentrationChange(old_state=3, new_state=4, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R(None, self.concentrations), [30])
        self.assertEqual(self.normal_two.R(None, self.concentrations), [40])

    def test_missing_rates(self):
        self.assertEqual(self.missing.R(None, self.concentrations), [0])

    def test_normal_perform(self):
        self.normal_one.perform(None, None, self.concentrations, None, None)
        self.assertEqual(self.concentrations[1].count, -1)
        self.assertEqual(self.concentrations[2].count,  1)

        self.normal_one.perform(None, None, self.concentrations, None, None)
        self.assertEqual(self.concentrations[1].count, -2)
        self.assertEqual(self.concentrations[2].count,  2)

        self.normal_two.perform(None, None, self.concentrations, None, None)
        self.assertEqual(self.concentrations[1].count, -2)
        self.assertEqual(self.concentrations[2].count,  1)
        self.assertEqual(self.concentrations[3].count,  1)

    def test_missing_perform(self):
        self.missing.perform(None, None, self.concentrations, None, None)
        self.assertEqual(self.concentrations[3].count, -1)
        self.assertEqual(self.concentrations[4].count,  1)


class ConcentrationChangeWithByproductTest(unittest.TestCase):
    def setUp(self):
        self.concentrations = defaultdict(MockConcentration)

        self.concentrations[1] = MockConcentration(value=10)
        self.concentrations[2] = MockConcentration(value=20)

        self.normal_one = ConcentrationChangeWithByproduct(old_state=1,
                new_state=2, byproduct=11, rate=3)
        self.normal_two = ConcentrationChangeWithByproduct(old_state=2,
                new_state=3, byproduct=12, rate=2)

        self.missing = ConcentrationChangeWithByproduct(old_state=3,
                new_state=4, byproduct=13, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R(None, self.concentrations), [30])
        self.assertEqual(self.normal_two.R(None, self.concentrations), [40])

    def test_missing_rates(self):
        self.assertEqual(self.missing.R(None, self.concentrations), [0])

    def test_normal_perform(self):
        self.normal_one.perform(None, None, self.concentrations, None, None)
        self.assertEqual(self.concentrations[1].count, -1)
        self.assertEqual(self.concentrations[2].count,  1)
        self.assertEqual(self.concentrations[11].count, 1)

        self.normal_one.perform(None, None, self.concentrations, None, None)
        self.assertEqual(self.concentrations[1].count, -2)
        self.assertEqual(self.concentrations[2].count,  2)
        self.assertEqual(self.concentrations[11].count, 2)

        self.normal_two.perform(None, None, self.concentrations, None, None)
        self.assertEqual(self.concentrations[1].count, -2)
        self.assertEqual(self.concentrations[2].count,  1)
        self.assertEqual(self.concentrations[3].count,  1)
        self.assertEqual(self.concentrations[12].count, 1)

    def test_missing_perform(self):
        self.missing.perform(None, None, self.concentrations, None, None)
        self.assertEqual(self.concentrations[3].count, -1)
        self.assertEqual(self.concentrations[4].count,  1)
        self.assertEqual(self.concentrations[13].count, 1)


if '__main__' == __name__:
    unittest.main()
