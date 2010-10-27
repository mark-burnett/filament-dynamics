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

from actin_dynamics.simulation import concentrations

class FixedReagentTest(unittest.TestCase):
    def test_typical_FixedReagent(self):
        fr = concentrations.FixedReagent(3.0, 0.1)

        self.assertEqual(3.0, fr.value)
        
        fr.add_monomer()
        self.assertEqual(3.1, fr.value)

        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        fr.remove_monomer()
        # Messy looking, but avoids rounding errors.
        self.assertEqual(3.0 - 0.1 - 0.1 - 0.1 - 0.1 - 0.1, fr.value)

        fr.add_monomer()
        fr.add_monomer()
        fr.add_monomer()
        # Messy looking, but avoids rounding errors.
        self.assertEqual(3.0 - 0.1 - 0.1, fr.value)

if '__main__' == __name__:
    unittest.main()
