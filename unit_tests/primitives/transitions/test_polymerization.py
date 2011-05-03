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

from actin_dynamics.primitives.transitions import polymerization

from actin_dynamics.state import single_strand_filaments
from actin_dynamics import simulation_strategy

from unit_tests.mocks.concentrations import MockConcentration

class BarbedPolymerizationSingleFilament(unittest.TestCase):
    def setUp(self):
        self.filaments = {
                'A': single_strand_filaments.Filament([None, None, None]),
                'B': single_strand_filaments.Filament([None, None, None])}

        self.concentrations = collections.defaultdict(MockConcentration)
        self.concentrations[1] = MockConcentration(value=3)
        self.concentrations[2] = MockConcentration(value=7)

        self.simulation_state = simulation_strategy.SimulationState(
                concentrations=self.concentrations, filaments=self.filaments)

        self.poly_one = polymerization.BarbedPolymerization(species=1, rate=1)
        self.poly_two = polymerization.BarbedPolymerization(species=2, rate=2)

    def test_rates(self):
        self.assertEqual(self.poly_one.R(None, self.simulation_state), 6)
        self.assertEqual(self.poly_two.R(None, self.simulation_state), 28)

    def test_perform(self):
        self.test_rates()
        self.poly_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, None, None, 1])

        self.poly_two.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, None, None, 1, 2])

        self.poly_one.perform(None, self.simulation_state, 0)
        self.assertEqual(list(self.filaments['A']), [None, None, None, 1, 2, 1])

        self.poly_two.perform(None, self.simulation_state, 14)
        self.assertEqual(list(self.filaments['B']), [None, None, None, 2])

        self.poly_one.perform(None, self.simulation_state, 0.36)
        self.assertEqual(list(self.filaments['A']), [None, None, None, 1, 2, 1, 1])

        self.poly_one.perform(None, self.simulation_state, 4.1)
        self.assertEqual(list(self.filaments['B']), [None, None, None, 2, 1])

        self.assertRaises(IndexError, self.poly_two.perform,
                None, self.simulation_state, 28)

        # Validate rates after some transitions.
        self.test_rates()

#class PointedPolymerization(unittest.TestCase):
#    def test_write_me_please(self):
#        self.assertTrue(False)

if '__main__' == __name__:
    unittest.main()
