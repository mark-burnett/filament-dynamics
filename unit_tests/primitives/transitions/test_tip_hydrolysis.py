#    Copyright (C) 2011 Mark Burnett
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

from actin_dynamics.primitives.transitions import tip_hydrolysis

from actin_dynamics.state import single_strand_filaments
from actin_dynamics import simulation_strategy

from unit_tests.mocks.concentrations import MockConcentration


class BarbedEndHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.filaments = {
                'A': single_strand_filaments.Filament([None, 1, 2, 1]),
                'B': single_strand_filaments.Filament([None, 2, 2, 1])}

        self.concentrations = collections.defaultdict(MockConcentration)

        self.simulation_state = simulation_strategy.SimulationState(
                concentrations=self.concentrations, filaments=self.filaments)

        self.hydro_one = tip_hydrolysis.BarbedEndHydrolysis(
                old_species=1, new_species=2, rate=1)
        self.hydro_two = tip_hydrolysis.BarbedEndHydrolysis(
                old_species=2, new_species=3, rate=2)

    def test_rates(self):
        self.assertEqual(self.hydro_one.R(None, self.simulation_state), 2)
        self.assertEqual(self.hydro_two.R(None, self.simulation_state), 0)

    def test_perform_first_filament(self):
        self.hydro_two.R(None, self.simulation_state)
        self.assertRaises(IndexError, self.hydro_two.perform,
                None, self.simulation_state, 0)

        self.hydro_one.R(None, self.simulation_state)
        self.hydro_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2, 2])
        self.assertEqual(list(self.filaments['B']), [None, 2, 2, 1])
        self.assertEqual(self.hydro_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.hydro_two.R(None, self.simulation_state), 2)

        self.hydro_one.R(None, self.simulation_state)
        self.hydro_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2, 2])
        self.assertEqual(list(self.filaments['B']), [None, 2, 2, 2])
        self.assertEqual(self.hydro_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.hydro_two.R(None, self.simulation_state), 4)

    def test_perform_second_filament(self):
        self.hydro_two.R(None, self.simulation_state)
        self.assertRaises(IndexError, self.hydro_two.perform,
                None, self.simulation_state, 0)

        self.hydro_one.R(None, self.simulation_state)
        self.hydro_one.perform(None, self.simulation_state, 1.1)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2, 1])
        self.assertEqual(list(self.filaments['B']), [None, 2, 2, 2])
        self.assertEqual(self.hydro_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.hydro_two.R(None, self.simulation_state), 2)

        self.hydro_one.R(None, self.simulation_state)
        self.hydro_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2, 2])
        self.assertEqual(list(self.filaments['B']), [None, 2, 2, 2])
        self.assertEqual(self.hydro_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.hydro_two.R(None, self.simulation_state), 4)

    def test_perform_second_filament_edge(self):
        self.hydro_two.R(None, self.simulation_state)
        self.assertRaises(IndexError, self.hydro_two.perform,
                None, self.simulation_state, 0)

        self.hydro_one.R(None, self.simulation_state)
        self.hydro_one.perform(None, self.simulation_state, 1)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2, 1])
        self.assertEqual(list(self.filaments['B']), [None, 2, 2, 2])
        self.assertEqual(self.hydro_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.hydro_two.R(None, self.simulation_state), 2)

        self.hydro_one.R(None, self.simulation_state)
        self.hydro_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2, 2])
        self.assertEqual(list(self.filaments['B']), [None, 2, 2, 2])
        self.assertEqual(self.hydro_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.hydro_two.R(None, self.simulation_state), 4)


if '__main__' == __name__:
    unittest.main()
