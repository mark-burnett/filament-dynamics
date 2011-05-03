#    Copyright (C) 2010-2011 Mark Burnett
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

import collections

from actin_dynamics.primitives.transitions import concentration_changes

from actin_dynamics import simulation_strategy

from unit_tests.mocks.concentrations import MockConcentration

class ConcentrationChangeTest(unittest.TestCase):
    def setUp(self):
        self.concentrations = collections.defaultdict(MockConcentration)
        self.simulation_state = simulation_strategy.SimulationState(
                concentrations=self.concentrations, filaments=None)

        self.concentrations[1] = MockConcentration(count=10)
        self.concentrations[2] = MockConcentration(count=20)

        self.normal_one = concentration_changes.ConcentrationChange(
                old_species=1, new_species=2, rate=3)
        self.normal_two = concentration_changes.ConcentrationChange(
                old_species=2, new_species=3, rate=2)

        self.missing = concentration_changes.ConcentrationChange(
                old_species=3, new_species=4, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R(None, self.simulation_state), 30)
        self.assertEqual(self.normal_two.R(None, self.simulation_state), 40)
        self.assertEqual(self.concentrations[1].monomer_access_count, 1)

    def test_missing_rates(self):
        self.assertEqual(self.missing.R(None, self.simulation_state), 0)
        self.assertEqual(self.concentrations[3].monomer_access_count, 1)

    def test_normal_perform(self):
        self.normal_one.R(None, self.simulation_state)
        self.normal_one.perform(None, self.simulation_state, None)
        self.assertEqual(self.concentrations[1]._count,  9)
        self.assertEqual(self.concentrations[2]._count, 21)

        self.normal_one.R(None, self.simulation_state)
        self.normal_one.perform(None, self.simulation_state, None)
        self.assertEqual(self.concentrations[1]._count,  8)
        self.assertEqual(self.concentrations[2]._count, 22)

        self.normal_two.R(None, self.simulation_state)
        self.normal_two.perform(None, self.simulation_state, None)
        self.assertEqual(self.concentrations[1]._count,  8)
        self.assertEqual(self.concentrations[2]._count, 21)
        self.assertEqual(self.concentrations[3]._count,  1)

    def test_missing_perform(self):
        self.missing.R(None, self.simulation_state)
        self.assertRaises(IndexError, self.missing.perform,
                None, self.simulation_state, None)


if '__main__' == __name__:
    unittest.main()
