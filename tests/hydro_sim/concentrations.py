import unittest

from hydro_sim import concentrations

class ConcentrationsTest(unittest.TestCase):
    def test_typical_FixedConcentration(self):
        values = [3.1, 0.0001, 7]
        for v in values:
            fc = concentrations.FixedConcentration(v)
            self.assertEqual(v, fc.value())

    def test_negative_FixedConcentration(self):
        self.assertRaises(ValueError, concentrations.FixedConcentration, -0.5)

    def test_ZeroConcentration(self):
        zc = concentrations.ZeroConcentration()
        self.assertEqual(0, zc.value())

    def test_typical_FixedReagent(self):
        fr = concentrations.FixedReagent(3.0, 0.1)

        self.assertEqual(3.0, fr.value())
        
        fr.add_monomer()
        self.assertEqual(3.1, fr.value())

        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        # Messy looking, but avoids rounding errors.
        self.assertEqual(3.0 - 0.1 - 0.1 - 0.1 - 0.1 - 0.1, fr.value())

        fr.add_monomer()
        fr.add_monomer()
        fr.add_monomer()
        # Messy looking, but avoids rounding errors.
        self.assertEqual(3.0 - 0.1 - 0.1, fr.value())

if '__main__' == __name__:
    unittest.main()
