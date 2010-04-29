import unittest
from util import observer

def passing_subscriber(event):
    pass

def raising_subscriber(event):
    raise RuntimeError('This subscriber breaks.')

class CountingSubscriber(object):
    def __init__(self):
        self.count = 0
    def __call__(self, event):
        self.count += 1

class ObserverTest(unittest.TestCase):
    def test_orthogonal_subscribers(self):
        # Setup some test data.
        events_to_test = [int, str, dict, set, list, float]
        event_counts   = [3, 1, 2, 1, 7, 4]
        subscribers = [CountingSubscriber() for e in events_to_test]

        # Subscribe to all the events.
        pub = observer.Publisher()
        for e, s in zip(events_to_test, subscribers):
            pub.subscribe(s, e)

        # Publish a bunch of events
        for e, c in zip(events_to_test, event_counts):
            for i in xrange(c):
                pub.publish(e())

        # Verify correct number of calls to each subscriber
        for s, c in zip(subscribers, event_counts):
            self.assertEqual(s.count, c)

    def test_overlapping_subscribers(self):
        # Test data.
        events = [[int, str], [int, float]]
        calls  = [int, str, str, int, float, str, float, int]
        total_counts = [(1, 1), (2, 1), (3, 1), (4, 2), (4, 3), (5, 3), (5, 4),
                        (6, 5)]

        # Subscribers
        subscribers = [CountingSubscriber() for elist in events]

        # Subscribe
        pub = observer.Publisher()
        for s, elist in zip(subscribers, events):
            map(lambda e: pub.subscribe(s, e), elist)

        for call, counts in zip(calls, total_counts):
            pub.publish(call())
            for s, count in zip(subscribers, counts):
                self.assertEqual(s.count, count)

    def test_unsubscribe(self):
        pub = observer.Publisher()
        sub = CountingSubscriber()

        # Subscribe to initial events.
        pub.subscribe(sub, int)
        pub.subscribe(sub, float)

        # Make sure that's working.
        pub.publish(1)
        pub.publish(2)
        self.assertEqual(2, sub.count)
        pub.publish(3.0)
        self.assertEqual(3, sub.count)

        # Remove one type of event.
        pub.unsubscribe(sub, int)
        pub.publish(4)

        # Make sure that's working.
        self.assertEqual(3, sub.count)
        pub.publish(5.0)
        self.assertEqual(4, sub.count)

        # Add a new type of event.
        pub.subscribe(sub, str)

        # Make sure that's working.
        pub.publish("6")
        self.assertEqual(5, sub.count)

        # Remove all.
        pub.unsubscribe(sub)

        # Make sure that's working.
        pub.publish(7)
        pub.publish(8.0)
        pub.publish("9")
        self.assertEqual(5, sub.count)

    def test_subscribe_arguments_reversed(self):
        pub = observer.Publisher()
        self.assertRaises(RuntimeError, pub.subscribe, int, passing_subscriber)

    def test_raising_subscriber(self):
        pub = observer.Publisher()
        pub.subscribe(raising_subscriber, int)
        self.assertRaises(RuntimeError, pub.publish, 3)

    def test_event_list(self):
        pub = observer.Publisher()
        self.assertEqual([], pub.events)
        sub = CountingSubscriber()

        pub.subscribe(sub, int)
        self.assertEqual([int], pub.events)
        pub.subscribe(sub, float)
        self.assertEqual(2, len(pub.events))

        pub.unsubscribe(sub, int)
        self.assertEqual([float], pub.events)

if '__main__' == __name__:
    unittest.main()
