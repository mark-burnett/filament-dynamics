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

from actin_dynamics.analysis import fitness

class TestFitnessVector(unittest.TestCase):
    def setUp(self):
        self.data = ['normal', 'squared']
        self.functions = [lambda ps, d: (ps, d),
                          lambda ps, d: (ps**2, d)]
        self.parameter_sets = range(5)

    def test_vector(self):
        expected_results = [[(ps, 'normal'), (ps**2, 'squared')]
                            for ps in self.parameter_sets]

        for i, ps in enumerate(self.parameter_sets):
            self.assertEqual(expected_results[i],
                    fitness.vector(ps, self.data, functions=self.functions))
