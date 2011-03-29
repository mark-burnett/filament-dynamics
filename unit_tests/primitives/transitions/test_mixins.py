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
from collections import defaultdict

from actin_dynamics.primitives.transitions.mixins import *
from actin_dynamics.state.single_strand_filaments import Filament

from unit_tests.mocks.concentrations import MockConcentration


class ByproductMixinTest(unittest.TestCase):
    def setUp(self):
        self.strand = Filament([1, 2, 3, 1, 2, 3, 1])
        self.concentrations = defaultdict(MockConcentration)

        self.mixin = WithByproduct(byproduct=11)

    def test_normal_perform(self):
        self.mixin.perform(None, self.strand, self.concentrations, None, None)
        self.assertEqual(self.concentrations[11].count, 1)

        self.mixin.perform(None, self.strand, self.concentrations, None, None)
        self.assertEqual(self.concentrations[11].count, 2)

        self.mixin.perform(None, self.strand, self.concentrations, None, None)
        self.assertEqual(self.concentrations[11].count, 3)


if '__main__' == __name__:
    unittest.main()
