import unittest

from kmc import simulation

class MockTransition(object):
    def __init__(self, add_value, rate):
        self.add_value = add_value
        self.R = rate

    def initialize(self, pub, state):
        self.state = state

    def perform(self, time, r):
        self.state[0] += self.add_value

class MockEndCondition(object):
    def __init__(self, max_count):
        self.max_count = max_count

    def initialize(self, pub, state):
        self.count = 0

    def __call__(self, time, state):
        self.count += 1
        if self.count > self.max_count:
            return True
        return False

class MockMeasurement(object):
    def __init__(self, label):
        self.label = label

    def initialize(self, pub, state):
        self.data = []
        self.perform(None, state)

    def perform(self, time, state):
        self.data.append(state[0])

class SimulationTest(unittest.TestCase):
    def test_single_simulation(self):
        transitions  = [MockTransition(1, 1)]
        measurements = [MockMeasurement('mock_measurement')]
        ecs          = [MockEndCondition(3)]

        sim = simulation.Simulation(transitions, measurements, ecs)

        final_state, data = sim.run([5])
        self.assertEqual([8], final_state)
        self.assertEqual(1, len(data))
        self.assertEqual(data['mock_measurement'], [5, 6, 7, 8])
    
    def test_multiple_measurements(self):
        transitions  = [MockTransition(1, 1)]
        measurements = [MockMeasurement('measurement_1'),
                        MockMeasurement('measurement_2')]
        ecs          = [MockEndCondition(3)]

        sim = simulation.Simulation(transitions, measurements, ecs)

        final_state, data = sim.run([5])
        self.assertEqual(2, len(data))
        self.assertEqual(data['measurement_1'], data['measurement_2'])
        self.assertEqual(data['measurement_1'], [5, 6, 7, 8])

    def test_double_transition_stochastic(self):
        """
        NOTE: This test is probabilistic.
        """
        transitions  = [MockTransition( 1, 1),
                        MockTransition(-1, 1)]
        measurements = []
        ecs          = [MockEndCondition(10000)]

        sim = simulation.Simulation(transitions, measurements, ecs)

        final_state, data = sim.run([10000])

        self.assertTrue(final_state[0] < 10201)
        self.assertTrue(final_state[0] > 9799)

    def test_triple_transition_stochastic(self):
        """
        NOTE: This test is probabilistic.
        """
        transitions  = [MockTransition( 1, 1),
                        MockTransition(-1, 0.5),
                        MockTransition(-1, 0.5)]
        measurements = []
        ecs          = [MockEndCondition(10000)]

        sim = simulation.Simulation(transitions, measurements, ecs)

        final_state, data = sim.run([10000])

        self.assertTrue(final_state[0] < 10201)
        self.assertTrue(final_state[0] > 9799)

    def test_typical_sequence(self):
        transitions1 = [MockTransition( 1, 1)]
        transitions2 = [MockTransition(-1, 1)]
        measurements = [MockMeasurement('mock_measurement')]
        ecs          = [MockEndCondition(3)]

        simulations = [simulation.Simulation(transitions1, measurements, ecs),
                       simulation.Simulation(transitions2, measurements, ecs)]
        sequence = simulation.SimulationSequence(simulations)

        data = sequence([5])
        self.assertEqual(data[0]['mock_measurement'], [5, 6, 7, 8])
        self.assertEqual(data[1]['mock_measurement'], [8, 7, 6, 5])

if '__main__' == __name__:
    unittest.main()
