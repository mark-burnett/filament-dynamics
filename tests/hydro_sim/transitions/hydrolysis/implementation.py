import unittest

from util import observer
from hydro_sim.transitions import events
from hydro_sim.transitions.hydrolysis import implementation
from hydro_sim.transitions.hydrolysis import predicates

class TruePredicate(object):
    def __init__(self):
        self.barbed_range  = 0
        self.pointed_range = 0

    def __call__(self, strand, index):
        return True

class EventMonitor(object):
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(event)

class HydrolysisImplementationTest(unittest.TestCase):
    def test_simlpified(self):
        strand = ['t', 't', 't', 't', 't']
        ht = implementation.Hydrolysis(TruePredicate(), 1, 'd')

        pub = observer.Publisher()
        ht.initialize(pub, strand)
        self.assertEqual(5, ht.R)

        em = EventMonitor()
        pub.subscribe(em.record, events.hydrolysis)

        ht.perform(None, 1.9)
        self.assertEqual(['t', 'd', 't', 't', 't'], strand)

        ht.perform(None, 3.2)
        self.assertEqual(['t', 'd', 't', 'd', 't'], strand)

        ht.perform(None, 0.7)
        self.assertEqual(['d', 'd', 't', 'd', 't'], strand)

        self.assertEqual([1, 3, 0], [e.position for e in em.events])

    def test_typical_alone(self):
        strand = ['t', 't', 't', 't', 't']
        ht = implementation.Hydrolysis(predicates.Random('t'), 1, 'd')

        pub = observer.Publisher()
        ht.initialize(pub, strand)
        self.assertEqual(5, ht.R)

        em = EventMonitor()
        pub.subscribe(em.record, events.hydrolysis)

        ht.perform(None, 1.9)
        self.assertEqual(['t', 'd', 't', 't', 't'], strand)
        self.assertEqual(4, ht.R)

        ht.perform(None, 2.6)
        self.assertEqual(['t', 'd', 't', 'd', 't'], strand)
        self.assertEqual(3, ht.R)

        ht.perform(None, 2.6)
        self.assertEqual(['t', 'd', 't', 'd', 'd'], strand)
        self.assertEqual(2, ht.R)

        self.assertEqual([1, 3, 4], [e.position for e in em.events])

    def test_random_poly_depoly(self):
        strand = ['t', 't', 't', 't', 't']
        ht = implementation.Hydrolysis(predicates.Random('t'), 1, 'd')

        pub = observer.Publisher()
        ht.initialize(pub, strand)
        self.assertEqual(5, ht.R)

        ht.perform(None, 1.9)
        self.assertEqual(['t', 'd', 't', 't', 't'], strand)
        self.assertEqual(4, ht.R)

        strand.append('t')
        pub.publish(events.polymerization('barbed', None, None))
        self.assertEqual(['t', 'd', 't', 't', 't', 't'], strand)
        self.assertEqual(5, ht.R)

        ht.perform(None, 4.1)
        self.assertEqual(['t', 'd', 't', 't', 't', 'd'], strand)
        self.assertEqual(4, ht.R)

        strand.pop()
        pub.publish(events.depolymerization('barbed', None, None))
        self.assertEqual(['t', 'd', 't', 't', 't'], strand)
        self.assertEqual(4, ht.R)

        strand.pop()
        pub.publish(events.depolymerization('barbed', None, None))
        self.assertEqual(['t', 'd', 't', 't'], strand)
        self.assertEqual(3, ht.R)

        strand.append('d')
        pub.publish(events.polymerization('barbed', None, None))
        self.assertEqual(['t', 'd', 't', 't', 'd'], strand)
        self.assertEqual(3, ht.R)

    def test_cooperative_poly_depoly(self):
        strand = ['d', 'd', 't', 't', 'd', 't', 't', 'd']
        ht = implementation.Hydrolysis(predicates.Cooperative('t', 'd'), 1, 'd')

        pub = observer.Publisher()
        ht.initialize(pub, strand)
        self.assertEqual(2, ht.R)

        ht.perform(None, 1.9)
        self.assertEqual(['d', 'd', 't', 't', 'd', 'd', 't', 'd'], strand)
        self.assertEqual(2, ht.R)

        strand.append('t')
        pub.publish(events.polymerization('barbed', None, None))
        self.assertEqual(3, ht.R)
        self.assertEqual(strand.count('t'), 4)

        ht.perform(None, 0.1)
        self.assertEqual(strand.count('t'), 3)

        ht.perform(None, 0.1)
        self.assertEqual(2, ht.R)
        self.assertEqual(strand.count('t'), 2)

        strand.pop()
        pub.publish(events.depolymerization('barbed', None, None))

        strand.pop()
        pub.publish(events.depolymerization('barbed', None, None))
        post_depoly_R = ht.R

        strand.append('d')
        pub.publish(events.polymerization('barbed', None, None))
        self.assertEqual(post_depoly_R, ht.R)

        strand.append('t')
        pub.publish(events.polymerization('barbed', None, None))
        self.assertEqual(post_depoly_R + 1, ht.R)

if '__main__' == __name__:
    unittest.main()
