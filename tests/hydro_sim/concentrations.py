import unittest

from hydro_sim import concentrations

class ConcentrationsTest(unittest.TestCase):
    def test_typical_fixed_concentration(self):
        values = [3.1, 0.0001, 7]
        for v in values:
            fc = concentrations.fixed_concentration(v)
            self.assertEqual(v, fc())

    def test_negative_fixed_concentration(self):
        self.assertRaises(ValueError, concentrations.fixed_concentration, -0.5)

    def test_zero_concentration(self):
        zc = concentrations.zero_concentration()
        self.assertEqual(0, zc())

    def test_typical_fixed_reagent(self):
        fr = concentrations.fixed_reagent(3.0, 0.1)
        fr.initialize()

        self.assertEqual(3.0, fr())
        
        fr.update_depoly(None)
        self.assertEqual(3.1, fr())

        fr.update_poly(None)
        fr.update_poly(None)
        fr.update_poly(None)
        fr.update_poly(None)
        fr.update_poly(None)
        fr.update_poly(None)
        # Messy looking, but avoids rounding errors.
        self.assertEqual(3.0 - 0.1 - 0.1 - 0.1 - 0.1 - 0.1, fr())


if '__main__' == __name__:
    unittest.main()
