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

from actin_dynamics.primitives.transitions import reverse_hydrolysis

from actin_dynamics.state import single_strand_filaments
from actin_dynamics import simulation_strategy

from unit_tests.mocks.concentrations import MockConcentration


class BarbedEndHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.filaments = {
                'A': single_strand_filaments.Filament([1, 2, 1]),
                'B': single_strand_filaments.Filament([2, 2, 1])}

        self.concentrations = {3: MockConcentration(value=2)}

        self.simulation_state = simulation_strategy.SimulationState(
                concentrations=self.concentrations, filaments=self.filaments)

        self.reverse_hydro = reverse_hydrolysis.ReverseHydrolysis(
                old_species=1, new_species=2, concentration=3, rate=3)

    def test_rates(self):
        self.assertEqual(self.reverse_hydro.R(None, self.simulation_state), 18)

    def test_perform_first_filament_first_element(self):
        self.reverse_hydro.R(None, self.simulation_state)
        self.reverse_hydro.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [2, 2, 1])
        self.assertEqual(list(self.filaments['B']), [2, 2, 1])
        self.assertEqual(self.concentrations[3].count, -1)

    def test_perform_first_filament_second_element(self):
        self.reverse_hydro.R(None, self.simulation_state)
        self.reverse_hydro.perform(None, self.simulation_state, 7.2)
        self.assertEqual(list(self.filaments['A']), [1, 2, 2])
        self.assertEqual(list(self.filaments['B']), [2, 2, 1])
        self.assertEqual(self.concentrations[3].count, -1)

    def test_perform_first_filament_second_element_edge(self):
        self.reverse_hydro.R(None, self.simulation_state)
        self.reverse_hydro.perform(None, self.simulation_state, 6)
        self.assertEqual(list(self.filaments['A']), [1, 2, 2])
        self.assertEqual(list(self.filaments['B']), [2, 2, 1])
        self.assertEqual(self.concentrations[3].count, -1)

    def test_perform_second_filament(self):
        self.reverse_hydro.R(None, self.simulation_state)
        self.reverse_hydro.perform(None, self.simulation_state, 14.2)
        self.assertEqual(list(self.filaments['A']), [1, 2, 1])
        self.assertEqual(list(self.filaments['B']), [2, 2, 2])
        self.assertEqual(self.concentrations[3].count, -1)


if '__main__' == __name__:
    unittest.main()
