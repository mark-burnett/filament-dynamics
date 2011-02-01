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
from actin_dynamics.run_support import report_measurements
from actin_dynamics.filaments.single_strand_filaments import Filament

from unit_tests.mocks.end_conditions import MockEndCondition
from unit_tests.mocks.measurements import MockMeasurement
from unit_tests.mocks.random_number_generators import MockRNG
from unit_tests.mocks.transitions import MockTransition


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

        run_simulation(sim)
        measurements = report_measurements(sim)
        sim_data = measurements['concentrations']
        final_state = [f['final_state'] for f in measurements['filaments']]
        filament_data = [f['measurements'] for f in measurements['filaments']]

        self.assertEqual([8], list(final_state[0]))
        self.assertEqual(0, len(sim_data))
        self.assertEqual(1, len(filament_data))
        times, values = filament_data[0]['mock_measurement']
        self.assertEqual(values, (5, 6, 7, 8))

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

        run_simulation(sim)
        measurements = report_measurements(sim)
        filament_data = [f['measurements'] for f in measurements['filaments']]

        self.assertEqual(2, len(filament_data[0]))
        self.assertEqual(filament_data[0]['measurement_1'],
                         filament_data[0]['measurement_2'])

        times, values = filament_data[0]['measurement_1']
        self.assertEqual(values, (5, 6, 7, 8))


#class DetailedSimulationTests(unittest.TestCase):
#    def test_detailed_logging_tests(self):
#        '''
#        Record the events that concentrations, transitions, ecs, and
#        measurements get.  Preferably each in their own test.
#        '''
#        self.assertTrue(False)


if '__main__' == __name__:
    unittest.main()