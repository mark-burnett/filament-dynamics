import unittest

from hydro_sim import measurements
from hydro_sim import strand

class MockConcentration(object):
    def remove_monomer(self):
        pass

    def add_monomer(self):
        pass

class MockState(object):
    def __init__(self, strand):
        self.strand = strand
        self.concentrations = {'t': MockConcentration(),
                               'd': MockConcentration(),
                               'p': MockConcentration()}

# Because the measurements operate/couple tightly with strand, we will use
# real strand objects for testing instead of mocks.

class TransitionCountTest(unittest.TestCase):
    def setUp(self):
        self.state = MockState(strand.Strand(['t', 'p', 'd'],
                            ['d', 'd', 'p', 'd', 'p', 't', 'p', 'd', 'p', 'p', 't', 't']))
    
    def tearDown(self):
        del self.state

    def test_initialization(self):
        m = measurements.TransitionCount(None, 't', 'p')
        self.assertEqual([(0,0)], m.data)

    def test_no_transition(self):
        m = measurements.TransitionCount(None, 't', 'p')

        m.perform(None, self.state)
        self.assertEqual([(0,0)], m.data)

    def test_append(self):
        m = measurements.TransitionCount(None, 't', 'p')
        m.perform(None, self.state)
        self.state.strand.append('t')

        m.perform(None, self.state)
        self.assertEqual([(0,0)], m.data)

    def test_pop(self):
        m = measurements.TransitionCount(None, 't', 'p')
        m.perform(None, self.state)
        self.state.strand.pop()

        m.perform(None, self.state)
        self.assertEqual([(0,0)], m.data)
        self.assertEqual(2, m._last_old_count)
        self.assertEqual(5, m._last_new_count)

    def test_matching_transition(self):
        m = measurements.TransitionCount(None, 't', 'p')
        m.perform(None, self.state)

        self.state.strand[5] = 'p'
        m.perform(None, self.state)
        self.assertEqual([(0,0), (None, 1)], m.data)

    def test_mismatched_transition(self):
        m = measurements.TransitionCount(None, 't', 'p')
        m.perform(None, self.state)

        self.state.strand[4] = 'd'
        m.perform(None, self.state)
        self.assertEqual([(0,0)], m.data)

    def test_matching_following_mismatched(self):
        m = measurements.TransitionCount(None, 't', 'p')
        m.perform(None, self.state)

        self.state.strand[4] = 'd'
        m.perform(None, self.state)

        self.state.strand[5] = 'p'
        m.perform(None, self.state)

        self.assertEqual([(0,0), (None, 1)], m.data)

    def test_match_match(self):
        m = measurements.TransitionCount(None, 't', 'p')
        m.perform(None, self.state)

        self.state.strand[5] = 'p'
        m.perform(None, self.state)

        self.state.strand[-2] = 'p'
        m.perform(None, self.state)

        self.assertEqual([(0,0), (None, 1), (None, 2)], m.data)


    def test_match_append_match(self):
        m = measurements.TransitionCount(None, 't', 'p')
        m.perform(None, self.state)

        self.state.strand[5] = 'p'
        m.perform(None, self.state)

        self.state.strand.append('t')
        m.perform(None, self.state)

        self.state.strand[-2] = 'p'
        m.perform(None, self.state)

        self.assertEqual([(0,0), (None, 1), (None, 2)], m.data)

if '__main__' == __name__:
    unittest.main()
