import unittest
import collections

from util import observer
from hydro_sim.transitions import events
from hydro_sim.transitions.depolymerization import fixed_rate

class EventCounter(object):
    def __init__(self):
        self.count = 0
    def __call__(self, event):
        self.count += 1

class FixedRateDepolymerizationTest(unittest.TestCase):
    def test_barbed(self):
        fr = fixed_rate.Barbed(None, 'd', 2.2)

        strand = ['n']
        pub = observer.Publisher()
        fr.initialize(pub, strand)

        ec = EventCounter()
        pub.subscribe(ec, events.depolymerization)

        self.assertEqual(0, ec.count)
        self.assertEqual(0, fr.R)

        strand.append('d')
        self.assertEqual(0, ec.count)
        self.assertEqual(2.2, fr.R)

        strand.append('d')
        strand.append('d')
        self.assertEqual(0, ec.count)
        self.assertEqual(2.2, fr.R)

        fr.perform(None, None)
        self.assertEqual(['n', 'd', 'd'], strand)
        self.assertEqual(1, ec.count)
        self.assertEqual(2.2, fr.R)

        fr.perform(None, None)
        self.assertEqual(['n', 'd'], strand)
        self.assertEqual(2, ec.count)
        self.assertEqual(2.2, fr.R)

        fr.perform(None, None)
        self.assertEqual(['n'], strand)
        self.assertEqual(3, ec.count)
        self.assertEqual(0, fr.R)

    def test_pointed(self):
        fr = fixed_rate.Pointed(None, 'd', 2.2)

        strand = collections.deque(['n'])
        pub = observer.Publisher()
        fr.initialize(pub, strand)

        ec = EventCounter()
        pub.subscribe(ec, events.depolymerization)

        self.assertEqual(0, ec.count)
        self.assertEqual(0, fr.R)

        strand.appendleft('d')
        self.assertEqual(0, ec.count)
        self.assertEqual(2.2, fr.R)

        strand.appendleft('d')
        strand.appendleft('d')
        self.assertEqual(0, ec.count)
        self.assertEqual(2.2, fr.R)

        fr.perform(None, None)
        self.assertEqual(collections.deque(['d', 'd', 'n']), strand)
        self.assertEqual(1, ec.count)
        self.assertEqual(2.2, fr.R)

        fr.perform(None, None)
        self.assertEqual(collections.deque(['d', 'n']), strand)
        self.assertEqual(2, ec.count)
        self.assertEqual(2.2, fr.R)

        fr.perform(None, None)
        self.assertEqual(collections.deque(['n']), strand)
        self.assertEqual(3, ec.count)
        self.assertEqual(0, fr.R)

if '__main__' == __name__:
    unittest.main()
