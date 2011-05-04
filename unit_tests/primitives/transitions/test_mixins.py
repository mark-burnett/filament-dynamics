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
import collections

from actin_dynamics.primitives.transitions import mixins
from actin_dynamics.state import single_strand_filaments

from actin_dynamics import simulation_strategy

from unit_tests.mocks.concentrations import MockConcentration


class ByproductMixinTest(unittest.TestCase):
    def setUp(self):
        self.concentrations = collections.defaultdict(MockConcentration)
        self.simulation_state = simulation_strategy.SimulationState(
                concentrations=self.concentrations, filaments=None)

        self.mixin = mixins.WithByproduct(byproduct=11)

    def test_normal_perform(self):
        self.mixin.perform(None, self.simulation_state, None)
        self.assertEqual(self.concentrations[11].count, 1)

        self.mixin.perform(None, self.simulation_state, None)
        self.assertEqual(self.concentrations[11].count, 2)

        self.mixin.perform(None, self.simulation_state, None)
        self.assertEqual(self.concentrations[11].count, 3)


if '__main__' == __name__:
    unittest.main()
