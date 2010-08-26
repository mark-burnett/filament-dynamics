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

from actin_dynamics.simulation.simulations import Simulation, running_total

from tests.mocks.end_conditions import MockEndCondition
from tests.mocks.explicit_measurements import MockExplicitMeasurement
from tests.mocks.random_number_generators import MockRNG
from tests.mocks.transitions import MockTransition
from tests.mocks.strand_factories import MockStrandFactory


class BasicSimulationTests(unittest.TestCase):
    def test_basic_simulation(self):
        transitions    = [MockTransition(1, 1)]
        concentrations = {}
        measurements   = [MockExplicitMeasurement('mock_measurement')]
        ecs            = [MockEndCondition(3)]
        strand_factory = MockStrandFactory([5])
        rng            = MockRNG(0.5)

        sim = Simulation(transitions, concentrations, measurements, ecs,
                         strand_factory, rng)

        final_state, data = sim.run()
        self.assertEqual([8], final_state)
        self.assertEqual(1, len(data))
        self.assertEqual(data['mock_measurement'], [6, 7, 8])

    def test_multiple_measurements(self):
        transitions    = [MockTransition(1, 1)]
        concentrations = {}
        measurements   = [MockExplicitMeasurement('measurement_1'),
                          MockExplicitMeasurement('measurement_2')]
        strand_factory = MockStrandFactory([5])
        ecs            = [MockEndCondition(3)]
        rng            = MockRNG(0.5)

        sim = Simulation(transitions, concentrations, measurements, ecs,
                         strand_factory, rng)

        final_state, data = sim.run()
        self.assertEqual(2, len(data))
        self.assertEqual(data['measurement_1'], data['measurement_2'])
        self.assertEqual(data['measurement_1'], [6, 7, 8])

class DetailedSimulationTests(unittest.TestCase):
    def test_detailed_logging_tests(self):
        '''
        Record the events that concentrations, transitions, ecs, and
        measurements get.  Preferably each in their own test.
        '''
        self.assertTrue(False)


class StochasticSimulationTests(unittest.TestCase):
    def test_double_transition_stochastic(self):
        """
        NOTE: This test is probabilistic.
        """
        transitions    = [MockTransition( 1, 1),
                          MockTransition(-1, 1)]
        concentrations = {}
        measurements   = []
        strand_factory = MockStrandFactory([1000])
        ecs            = [MockEndCondition(1000)]
        rng            = random.uniform

        sim = Simulation(transitions, concentrations, measurements, ecs,
                         strand_factory, rng)

        final_state, data = sim.run()

        self.assertTrue(final_state[0] < 1064)
        self.assertTrue(final_state[0] > 936)

    def test_unbalanced_transition_stochastic(self):
        """
        NOTE: This test is probabilistic.
        """
        transitions    = [MockTransition( 1, 1),
                          MockTransition(-1, 0.5)]
        concentrations = {}
        measurements   = []
        strand_factory = MockStrandFactory([1000])
        ecs            = [MockEndCondition(1000)]
        rng            = random.uniform

        sim = Simulation(transitions, concentrations, measurements, ecs,
                         strand_factory, rng)

        final_state, data = sim.run()

        self.assertTrue(final_state[0] < 1397)
        self.assertTrue(final_state[0] > 1270)

    def test_triple_transition_stochastic(self):
        """
        NOTE: This test is probabilistic.
        """
        transitions    = [MockTransition( 1, 1),
                          MockTransition(-1, 0.5),
                          MockTransition(-1, 0.5)]
        concentrations = {}
        measurements   = []
        strand_factory = MockStrandFactory([1000])
        ecs            = [MockEndCondition(1000)]
        rng            = random.uniform

        sim = Simulation(transitions, concentrations, measurements, ecs,
                         strand_factory, rng)

        final_state, data = sim.run()

        self.assertTrue(final_state[0] < 1064)
        self.assertTrue(final_state[0] > 936)


class RunningTotalTest(unittest.TestCase):
    def test_running_total(self):
        test_data = [[0, 1, 2, 3, 4, 5],
                     [7, 1, 2, 8],
                     [-5, 0, -2, 3]]
        answers   = [[0, 1, 3, 6, 10, 15],
                     [7, 8, 10, 18],
                     [-5, -5, -7, -4]]
        for a, d in zip(answers, test_data):
            self.assertEqual(a, list(running_total(d)))

if '__main__' == __name__:
    unittest.main()
