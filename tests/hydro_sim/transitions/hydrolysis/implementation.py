import unittest

from util import observer
from hydro_sim import events
from hydro_sim.transitions.hydrolysis import implementation
from hydro_sim.transitions.hydrolysis import predicates

from hydro_sim.state import State

class MockPublisher(object):
    def subscribe(self, a, b):
        pass

class TruePredicate(object):
    def __init__(self):
        pass

    def full_count(self, strand):
        return len(strand)

    def update_vicinity(self, strand, index):
        return 1

class EventMonitor(object):
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(event)

class MockStrand(list):
    def change_state(self, index, new_state, time):
        self[index] = new_state

class HydrolysisImplementationTest(unittest.TestCase):
#    def test_simlpified(self):
#        strand = MockStrand(['t', 't', 't', 't', 't'])
#        ht = implementation.Hydrolysis(TruePredicate(), 1, 'd')
#
#        ht.initialize(MockPublisher(), strand)
#
#        self.assertEqual(5, ht.R(strand))
#
#        ht.perform(None, strand, 1.9)
#        self.assertEqual(['t', 'd', 't', 't', 't'], strand)
#
#        ht.perform(None, strand, 3.2)
#        self.assertEqual(['t', 'd', 't', 'd', 't'], strand)
#
#        ht.perform(None, strand, 0.7)
#        self.assertEqual(['d', 'd', 't', 'd', 't'], strand)

    def test_typical_alone(self):
        strand = State(['t', 'd'], ['t', 't', 't', 't', 't'], {})
        ht = implementation.Random('t', 1, 'd')

        pub = observer.Publisher()
        strand.initialize(pub)
        ht.initialize(pub, strand)
        self.assertEqual(5, ht.R(strand))

        ht.perform(None, strand, 1.9)
        self.assertEqual(['t', 'd', 't', 't', 't'], strand.strand)
        self.assertEqual(4, ht.R(strand))

        ht.perform(None, strand, 2.6)
        self.assertEqual(['t', 'd', 't', 'd', 't'], strand.strand)
        self.assertEqual(3, ht.R(strand))

        ht.perform(None, strand, 2.6)
        self.assertEqual(['t', 'd', 't', 'd', 'd'], strand.strand)
        self.assertEqual(2, ht.R(strand))

#    def test_random_poly_depoly(self):
#        strand = ['t', 't', 't', 't', 't']
#        ht = implementation.Hydrolysis(predicates.Random('t'), 1, 'd')
#
#        pub = observer.Publisher()
#        ht.initialize(pub, strand)
#        self.assertEqual(5, ht.R)
#
#        ht.perform(None, 1.9)
#        self.assertEqual(['t', 'd', 't', 't', 't'], strand)
#        self.assertEqual(4, ht.R)
#
#        strand.append('t')
#        pub.publish(events.polymerization('barbed', None, None))
#        self.assertEqual(['t', 'd', 't', 't', 't', 't'], strand)
#        self.assertEqual(5, ht.R)
#
#        ht.perform(None, 4.1)
#        self.assertEqual(['t', 'd', 't', 't', 't', 'd'], strand)
#        self.assertEqual(4, ht.R)
#
#        strand.pop()
#        pub.publish(events.depolymerization('barbed', None, None))
#        self.assertEqual(['t', 'd', 't', 't', 't'], strand)
#        self.assertEqual(4, ht.R)
#
#        strand.pop()
#        pub.publish(events.depolymerization('barbed', None, None))
#        self.assertEqual(['t', 'd', 't', 't'], strand)
#        self.assertEqual(3, ht.R)
#
#        strand.append('d')
#        pub.publish(events.polymerization('barbed', None, None))
#        self.assertEqual(['t', 'd', 't', 't', 'd'], strand)
#        self.assertEqual(3, ht.R)
#
#    def test_cooperative_poly_depoly(self):
#        strand = ['d', 'd', 't', 't', 'd', 't', 't', 'd']
#        ht = implementation.Hydrolysis(predicates.Cooperative('t', 'd'), 1, 'd')
#
#        pub = observer.Publisher()
#        ht.initialize(pub, strand)
#        self.assertEqual(2, ht.R)
#
#        ht.perform(None, 1.9)
#        self.assertEqual(['d', 'd', 't', 't', 'd', 'd', 't', 'd'], strand)
#        self.assertEqual(2, ht.R)
#
#        strand.append('t')
#        pub.publish(events.polymerization('barbed', None, None))
#        self.assertEqual(3, ht.R)
#        self.assertEqual(strand.count('t'), 4)
#
#        ht.perform(None, 0.1)
#        self.assertEqual(strand.count('t'), 3)
#
#        ht.perform(None, 0.1)
#        self.assertEqual(2, ht.R)
#        self.assertEqual(strand.count('t'), 2)
#
#        strand.pop()
#        pub.publish(events.depolymerization('barbed', None, None))
#
#        strand.pop()
#        pub.publish(events.depolymerization('barbed', None, None))
#        post_depoly_R = ht.R
#
#        strand.append('d')
#        pub.publish(events.polymerization('barbed', None, None))
#        self.assertEqual(post_depoly_R, ht.R)
#
#        strand.append('t')
#        pub.publish(events.polymerization('barbed', None, None))
#        self.assertEqual(post_depoly_R + 1, ht.R)

if '__main__' == __name__:
    unittest.main()
