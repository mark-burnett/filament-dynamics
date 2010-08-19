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

from actin_dynamics.simulation.transitions.base_classes import Transition

class TransitionCountTest(unittest.TestCase):
    def test_initialization(self):
        test_label = 'test label text'
        t = Transition(measurement_label=test_label)
        self.assertEqual(test_label, t.measurement_label)
        self.assertEqual([(0, 0)], t.data)

    def test_perform(self):
        test_times = [7, 3, 1, 12]

        transition = Transition()
        self.assertEqual([(0, 0)], transition.data)

        for count, time in enumerate(test_times):
            transition.perform(time, None, None, None)
            self.assertEqual((time, count + 1), transition.data[-1])

        self.assertEqual([(t, c) for c, t in enumerate([0] + test_times)],
                         transition.data)

if '__main__' == __name__:
    unittest.main()
