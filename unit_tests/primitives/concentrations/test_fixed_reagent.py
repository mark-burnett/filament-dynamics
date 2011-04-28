#    Copyright (C) 2010 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from actin_dynamics.primitives.concentrations import fixed_reagent

class FixedReagentTest(unittest.TestCase):
    def test_typical_FixedReagent(self):
        initial_concentration = 3.0
        concentration_per_monomer = 0.1
        fr = fixed_reagent.FixedReagent(initial_concentration,
                                         concentration_per_monomer, number=1)
        original_monomer_count = int(initial_concentration
                                     / concentration_per_monomer)

        self.assertEqual(initial_concentration, fr.value(None))
        
        fr.add_monomer()
        self.assertEqual((original_monomer_count+1) * concentration_per_monomer,
                         fr.value(None))

        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        # Messy looking, but avoids rounding errors.
        self.assertEqual((original_monomer_count-5) * concentration_per_monomer,
                          fr.value(None))

        fr.add_monomer()
        fr.add_monomer()
        fr.add_monomer()
        # Messy looking, but avoids rounding errors.
        self.assertEqual((original_monomer_count-2) * concentration_per_monomer,
                          fr.value(None))

if '__main__' == __name__:
    unittest.main()
