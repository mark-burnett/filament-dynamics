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

from actin_dynamics.primitives.transitions import vectorial_hydrolysis
from actin_dynamics.state.single_strand_filaments import Filament

from unit_tests.mocks.concentrations import MockConcentration

from actin_dynamics import simulation_strategy


class VectorialHydrolysisTest(unittest.TestCase):
    def setUp(self):
        self.filaments = {'A': Filament([1, 2, 3, 1, 2, 3, 1]),
                          'B': Filament([3, 1, 2, 3, 1, 2, 3])}
        self.simulation_state = simulation_strategy.SimulationState(
                concentrations=None, filaments=self.filaments)

        self.normal_one = vectorial_hydrolysis.VectorialHydrolysis(
                old_species=1, pointed_neighbor=3, new_species=2, rate=3)
        self.normal_two = vectorial_hydrolysis.VectorialHydrolysis(
                old_species=2, pointed_neighbor=1, new_species=3, rate=2)
        self.missing    = vectorial_hydrolysis.VectorialHydrolysis(
                old_species=1, pointed_neighbor=2, new_species=7, rate=1)

    def test_normal_rates(self):
        self.assertEqual(self.normal_one.R(None, self.simulation_state), 12)
        self.assertEqual(self.normal_two.R(None, self.simulation_state),  8)

    def test_missing_rates(self):
        self.assertEqual(self.missing.R(None, self.simulation_state), 0)

    def test_perform_first_filament_first_element(self):
        self.normal_two.R(None, self.simulation_state)
        self.normal_two.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [1, 3, 3, 1, 2, 3, 1])
        self.assertEqual(list(self.filaments['B']), [3, 1, 2, 3, 1, 2, 3])

    def test_perform_first_filament_second_element(self):
        self.normal_two.R(None, self.simulation_state)
        self.normal_two.perform(None, self.simulation_state, 2.3)
        self.assertEqual(list(self.filaments['A']), [1, 2, 3, 1, 3, 3, 1])
        self.assertEqual(list(self.filaments['B']), [3, 1, 2, 3, 1, 2, 3])

    def test_perform_first_filament_second_element_edge(self):
        self.normal_two.R(None, self.simulation_state)
        self.normal_two.perform(None, self.simulation_state, 2)
        self.assertEqual(list(self.filaments['A']), [1, 2, 3, 1, 3, 3, 1])
        self.assertEqual(list(self.filaments['B']), [3, 1, 2, 3, 1, 2, 3])


    def test_perform_second_filament_first_element(self):
        self.normal_two.R(None, self.simulation_state)
        self.normal_two.perform(None, self.simulation_state, 4.1)
        self.assertEqual(list(self.filaments['A']), [1, 2, 3, 1, 2, 3, 1])
        self.assertEqual(list(self.filaments['B']), [3, 1, 3, 3, 1, 2, 3])

    def test_perform_second_filament_edge_first_element(self):
        self.normal_two.R(None, self.simulation_state)
        self.normal_two.perform(None, self.simulation_state, 4)
        self.assertEqual(list(self.filaments['A']), [1, 2, 3, 1, 2, 3, 1])
        self.assertEqual(list(self.filaments['B']), [3, 1, 3, 3, 1, 2, 3])

    def test_perform_second_filament_second_element(self):
        self.normal_two.R(None, self.simulation_state)
        self.normal_two.perform(None, self.simulation_state, 6.3)
        self.assertEqual(list(self.filaments['A']), [1, 2, 3, 1, 2, 3, 1])
        self.assertEqual(list(self.filaments['B']), [3, 1, 2, 3, 1, 3, 3])

    def test_perform_second_filament_second_element_edge(self):
        self.normal_two.R(None, self.simulation_state)
        self.normal_two.perform(None, self.simulation_state, 6)
        self.assertEqual(list(self.filaments['A']), [1, 2, 3, 1, 2, 3, 1])
        self.assertEqual(list(self.filaments['B']), [3, 1, 2, 3, 1, 3, 3])


if '__main__' == __name__:
    unittest.main()
