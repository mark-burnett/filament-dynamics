import unittest

from hydro_sim.transitions.hydrolysis import predicates

class PredicatesTest(unittest.TestCase):
    def test_typical_random(self):
        strand   = ['t', 'd', 'p', 't', 'p', 'd', 'd', 'p', 'd']
        result_t = [1, 0, 0, 1, 0, 0, 0, 0, 0]
        result_p = [0, 0, 1, 0, 1, 0, 0, 1, 0]
        result_d = [0, 1, 0, 0, 0, 1, 1, 0, 1]
        pred_t = predicates.Random('t')
        pred_p = predicates.Random('p')
        pred_d = predicates.Random('d')

        self.assertEqual(result_t, [pred_t(strand, i) for i in xrange(len(strand))])
        self.assertEqual(result_p, [pred_p(strand, i) for i in xrange(len(strand))])
        self.assertEqual(result_d, [pred_d(strand, i) for i in xrange(len(strand))])

    def test_typical_cooperative(self):
        strand    = ['t', 'd', 'p', 't', 'p', 'd', 'd', 'p', 'd']
        result_tp = [0, 0, 0, 1, 0, 0, 0, 0, 0]
        result_pd = [0, 0, 1, 0, 0, 0, 0, 1, 0]
        result_dp = [0, 0, 0, 0, 0, 1, 0, 0, 1]
        pred_tp = predicates.Cooperative('t', 'p')
        pred_pd = predicates.Cooperative('p', 'd')
        pred_dp = predicates.Cooperative('d', 'p')

        self.assertEqual(result_tp, [pred_tp(strand, i) for i in xrange(len(strand))])
        self.assertEqual(result_pd, [pred_pd(strand, i) for i in xrange(len(strand))])
        self.assertEqual(result_dp, [pred_dp(strand, i) for i in xrange(len(strand))])

if '__main__' == __name__:
    unittest.main()
