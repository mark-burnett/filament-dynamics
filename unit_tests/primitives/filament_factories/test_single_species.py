#    Copyright (C) 2011 Mark Burnett
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

from actin_dynamics.primitives.filament_factories import single_species

class SingleSpeciesFixedLengthTest(unittest.TestCase):
    def setUp(self):
        self.filament_factory = single_species.SingleSpeciesFixedLength(
                species='a', length=3, number=7)

    def test_create(self):
        filaments = self.filament_factory.create()

        self.assertEqual(7, len(filaments))
        for f in filaments:
            self.assertEqual(['a', 'a', 'a'], list(f))


if '__main__' == __name__:
    unittest.main()
