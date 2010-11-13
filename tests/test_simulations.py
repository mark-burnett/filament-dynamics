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

import random

import unittest

from actin_dynamics.simulations import Simulation, run_simulation
from actin_dynamics.filaments.single_strand_filaments import Filament

from tests.mocks.end_conditions import MockEndCondition
from tests.mocks.measurements import MockMeasurement
from tests.mocks.random_number_generators import MockRNG
from tests.mocks.transitions import MockTransition


class BasicSimulationTests(unittest.TestCase):
    def test_basic_simulation(self):
        transitions    = [MockTransition(1, 1)]
        concentrations = {}
        measurements   = [MockMeasurement('mock_measurement')]
        ecs            = [MockEndCondition(3)]
        filaments      = [Filament([5])]
        rng            = MockRNG(0.5)

        sim = Simulation(transitions=transitions, concentrations=concentrations,
                         measurements=measurements, end_conditions=ecs,
                         filaments=filaments, rng=rng)

        pars, sim_data, final_state, filament_data = run_simulation(sim)

        self.assertEqual([8], list(final_state[0]))
        self.assertEqual(0, len(sim_data))
        self.assertEqual(1, len(filament_data))
        values = [l for t, l in filament_data[0]['mock_measurement']]
        self.assertEqual(values, [5, 6, 7, 8])

    def test_multiple_measurements(self):
        transitions    = [MockTransition(1, 1)]
        concentrations = {}
        measurements   = [MockMeasurement('measurement_1'),
                          MockMeasurement('measurement_2')]
        filaments      = [Filament([5])]
        ecs            = [MockEndCondition(3)]
        rng            = MockRNG(0.5)

        sim = Simulation(transitions=transitions, concentrations=concentrations,
                         measurements=measurements, end_conditions=ecs,
                         filaments=filaments, rng=rng)

        pars, sim_data, final_state, filament_data = run_simulation(sim)

        self.assertEqual(2, len(filament_data[0]))
        self.assertEqual(filament_data[0]['measurement_1'], filament_data[0]['measurement_2'])

        values = [l for t, l in filament_data[0]['measurement_1']]
        self.assertEqual(values, [5, 6, 7, 8])

#class DetailedSimulationTests(unittest.TestCase):
#    def test_detailed_logging_tests(self):
#        '''
#        Record the events that concentrations, transitions, ecs, and
#        measurements get.  Preferably each in their own test.
#        '''
#        self.assertTrue(False)
#
#
#class StochasticSimulationTests(unittest.TestCase):
#    def test_double_transition_stochastic(self):
#        """
#        NOTE: This test is probabilistic.
#        """
#        transitions    = [MockTransition( 1, 1),
#                          MockTransition(-1, 1)]
#        concentrations = {}
#        measurements   = []
#        strand_factory = MockStrandFactory([1000])
#        ecs            = [MockEndCondition(1000)]
#        rng            = random.uniform
#
#        sim = Simulation(transitions, concentrations, measurements, ecs,
#                         strand_factory, rng)
#
#        final_state, data = sim.run()
#
#        self.assertTrue(final_state[0] < 1064)
#        self.assertTrue(final_state[0] > 936)
#
#    def test_unbalanced_transition_stochastic(self):
#        """
#        NOTE: This test is probabilistic.
#        """
#        transitions    = [MockTransition( 1, 1),
#                          MockTransition(-1, 0.5)]
#        concentrations = {}
#        measurements   = []
#        strand_factory = MockStrandFactory([1000])
#        ecs            = [MockEndCondition(1000)]
#        rng            = random.uniform
#
#        sim = Simulation(transitions, concentrations, measurements, ecs,
#                         strand_factory, rng)
#
#        final_state, data = sim.run()
#
#        self.assertTrue(final_state[0] < 1397)
#        self.assertTrue(final_state[0] > 1270)
#
#    def test_triple_transition_stochastic(self):
#        """
#        NOTE: This test is probabilistic.
#        """
#        transitions    = [MockTransition( 1, 1),
#                          MockTransition(-1, 0.5),
#                          MockTransition(-1, 0.5)]
#        concentrations = {}
#        measurements   = []
#        strand_factory = MockStrandFactory([1000])
#        ecs            = [MockEndCondition(1000)]
#        rng            = random.uniform
#
#        sim = Simulation(transitions, concentrations, measurements, ecs,
#                         strand_factory, rng)
#
#        final_state, data = sim.run()
#
#        self.assertTrue(final_state[0] < 1064)
#        self.assertTrue(final_state[0] > 936)


if '__main__' == __name__:
    unittest.main()
