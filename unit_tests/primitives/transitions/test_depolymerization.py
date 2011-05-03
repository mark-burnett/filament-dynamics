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

from actin_dynamics.primitives.transitions import depolymerization

from actin_dynamics.state import single_strand_filaments
from actin_dynamics import simulation_strategy

from unit_tests.mocks.concentrations import MockConcentration

class BarbedDepolymerizationSingleFilament(unittest.TestCase):
    def setUp(self):
        self.filaments = {
                'A': single_strand_filaments.Filament([None, 1, 2, 1]),
                'B': single_strand_filaments.Filament([None, 0, 2, 1])}
        self.concentrations = collections.defaultdict(MockConcentration)

        self.simulation_state = simulation_strategy.SimulationState(
                concentrations=self.concentrations,
                filaments=self.filaments)

        self.depoly_one = depolymerization.BarbedDepolymerization(species=1,
                                                                  rate=1)
        self.depoly_two = depolymerization.BarbedDepolymerization(species=2,
                                                                  rate=2)

    def test_rates(self):
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 2)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 0)

    def test_perform_first_filament(self):
        self.test_rates() # Calculate rates to initiate caching.

        # Depolymerize from first filament where both are possible
        self.depoly_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2])
        self.assertEqual(list(self.filaments['B']), [None, 0, 2, 1])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 2)

        self.depoly_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2])
        self.assertEqual(list(self.filaments['B']), [None, 0, 2])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 4)

    def test_perform_second_filament(self):
        self.test_rates() # Calculate rates to initiate caching.

        # Depolymerize from first filament where both are possible
        self.depoly_one.perform(None, self.simulation_state, 1.2)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2, 1])
        self.assertEqual(list(self.filaments['B']), [None, 0, 2])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 2)

        self.depoly_one.perform(None, self.simulation_state, 0.1)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2])
        self.assertEqual(list(self.filaments['B']), [None, 0, 2])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 4)

    def test_perform_second_filament_edge_case(self):
        self.test_rates() # Calculate rates to initiate caching.

        # Depolymerize from first filament where both are possible
        self.depoly_one.perform(None, self.simulation_state, 1)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2, 1])
        self.assertEqual(list(self.filaments['B']), [None, 0, 2])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 2)

        self.depoly_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, 1, 2])
        self.assertEqual(list(self.filaments['B']), [None, 0, 2])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 4)


class PointedDepolymerizationSingleFilament(unittest.TestCase):
    def setUp(self):
        self.filaments = {
                'A': single_strand_filaments.Filament([1, 2, 1, None]),
                'B': single_strand_filaments.Filament([1, 2, 0, None])}
        self.concentrations = collections.defaultdict(MockConcentration)

        self.simulation_state = simulation_strategy.SimulationState(
                concentrations=self.concentrations,
                filaments=self.filaments)

        self.depoly_one = depolymerization.PointedDepolymerization(species=1,
                                                                  rate=1)
        self.depoly_two = depolymerization.PointedDepolymerization(species=2,
                                                                  rate=2)

    def test_rates(self):
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 2)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 0)

    def test_perform_first_filament(self):
        self.test_rates() # Calculate rates to initiate caching.

        # Depolymerize from first filament where both are possible
        self.depoly_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [2, 1, None])
        self.assertEqual(list(self.filaments['B']), [1, 2, 0, None])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 2)

        self.depoly_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [2, 1, None])
        self.assertEqual(list(self.filaments['B']), [2, 0, None])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 4)

    def test_perform_second_filament(self):
        self.test_rates() # Calculate rates to initiate caching.

        # Depolymerize from first filament where both are possible
        self.depoly_one.perform(None, self.simulation_state, 1.2)
        self.assertEqual(list(self.filaments['A']), [1, 2, 1, None])
        self.assertEqual(list(self.filaments['B']), [2, 0, None])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 2)

        self.depoly_one.perform(None, self.simulation_state, 0.1)
        self.assertEqual(list(self.filaments['A']), [2, 1, None])
        self.assertEqual(list(self.filaments['B']), [2, 0, None])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 4)

    def test_perform_second_filament_edge_case(self):
        self.test_rates() # Calculate rates to initiate caching.

        # Depolymerize from first filament where both are possible
        self.depoly_one.perform(None, self.simulation_state, 1)
        self.assertEqual(list(self.filaments['A']), [1, 2, 1, None])
        self.assertEqual(list(self.filaments['B']), [2, 0, None])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 1)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 2)

        self.depoly_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [2, 1, None])
        self.assertEqual(list(self.filaments['B']), [2, 0, None])
        self.assertEqual(self.depoly_one.R(None, self.simulation_state), 0)
        self.assertEqual(self.depoly_two.R(None, self.simulation_state), 4)


if '__main__' == __name__:
    unittest.main()
