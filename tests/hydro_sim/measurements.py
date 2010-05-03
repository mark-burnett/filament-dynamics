import unittest

from hydro_sim import measurements

# Use a real publisher object
from util import observer
from hydro_sim.transitions import events

class MeasurementTest(unittest.TestCase):
    def test_typical_transition_event_counter(self):
        old_states = ['t', 'p']
        new_states = ['p', 'd']
        tc = measurements.TransitionEventCount('name', old_states, new_states)
        pub = observer.Publisher()
        tc.initialize(pub, None)

        test_events = [events.hydrolysis('t', 'p', None, None),
                       events.hydrolysis('p', 'p', None, None),
                       events.hydrolysis('p', 'd', None, None),
                       events.hydrolysis('d', 'd', None, None),
                       events.hydrolysis('d', 'p', None, None),
                       events.hydrolysis('d', 't', None, None),
                       events.hydrolysis('s', 's', None, None),
                       events.hydrolysis('a', 'b', None, None),
                       events.hydrolysis( 1,   2,  None, None)]
        counts = [1, 2, 3, 3, 3, 3, 3, 3, 3]
        for e, count in zip(test_events, counts):
            pub.publish(e)
            self.assertEqual(count, tc.data[-1][1])


if '__main__' == __name__:
    unittest.main()
