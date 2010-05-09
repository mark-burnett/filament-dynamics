import unittest

from hydro_sim import measurements

# Use a real publisher object
from util import observer
from hydro_sim import events

class MeasurementTest(unittest.TestCase):
    def test_typical_transition_event_counter(self):
        old_states = ['t', 'p']
        new_states = ['p', 'd']
        tc = measurements.TransitionEventCount('name', old_states, new_states)
        pub = observer.Publisher()
        tc.initialize(pub, None)

        test_events = [events.state_change(None, 't', 'p', None),
                       events.state_change(None, 'p', 'p', None),
                       events.state_change(None, 'p', 'd', None),
                       events.state_change(None, 'd', 'd', None),
                       events.state_change(None, 'd', 'p', None),
                       events.state_change(None, 'd', 't', None),
                       events.state_change(None, 's', 's', None),
                       events.state_change(None, 'a', 'b', None),
                       events.state_change(None,  1,   2 , None)]
        counts = [1, 2, 3, 3, 3, 3, 3, 3, 3]
        for e, count in zip(test_events, counts):
            pub.publish(e)
            self.assertEqual(count, tc.data[-1][1])


if '__main__' == __name__:
    unittest.main()
