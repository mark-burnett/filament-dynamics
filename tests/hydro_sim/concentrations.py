import unittest

from hydro_sim import concentrations

class ConcentrationsTest(unittest.TestCase):
    def test_typical_fixed_concentration(self):
        values = [3.1, 0.0001, 7]
        for v in values:
            fc = concentrations.fixed_concentration(v)
            self.assertEqual(v, fc.value())

    def test_negative_fixed_concentration(self):
        self.assertRaises(ValueError, concentrations.fixed_concentration, -0.5)

    def test_zero_concentration(self):
        zc = concentrations.zero_concentration()
        self.assertEqual(0, zc.value())

    def test_typical_fixed_reagent(self):
        fr = concentrations.fixed_reagent(3.0, 0.1)

        self.assertEqual(3.0, fr.value())
        
        fr.depolymerize()
        self.assertEqual(3.1, fr.value())

        fr.polymerize()
        fr.polymerize()
        fr.polymerize()
        fr.polymerize()
        fr.polymerize()
        fr.polymerize()
        # Messy looking, but avoids rounding errors.
        self.assertEqual(3.0 - 0.1 - 0.1 - 0.1 - 0.1 - 0.1, fr.value())

        fr.depolymerize()
        fr.depolymerize()
        fr.depolymerize()
        # Messy looking, but avoids rounding errors.
        self.assertEqual(3.0 - 0.1 - 0.1, fr.value())

if '__main__' == __name__:
    unittest.main()
