import unittest
import collections

from hydro_sim.transitions.depolymerization import fixed_rate

class FixedRateDepolymerizationTest(unittest.TestCase):
    def test_barbed(self):
        fr = fixed_rate.Barbed('d', 2.2)

        strand = ['n']
        self.assertEqual(0, fr.R(strand))

        strand.append('d')
        self.assertEqual(2.2, fr.R(strand))

        strand.append('d')
        strand.append('d')
        self.assertEqual(2.2, fr.R(strand))

        fr.perform(None, strand, None)
        self.assertEqual(['n', 'd', 'd'], strand)
        self.assertEqual(2.2, fr.R(strand))

        fr.perform(None, strand, None)
        self.assertEqual(['n', 'd'], strand)
        self.assertEqual(2.2, fr.R(strand))

        fr.perform(None, strand, None)
        self.assertEqual(['n'], strand)
        self.assertEqual(0, fr.R(strand))

if '__main__' == __name__:
    unittest.main()
