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

from actin_dynamics.simulation import end_conditions

class StateLengthBelowTest(unittest.TestCase):
    def test_vary_state(self):
        lengths     = [0, 5, 6, 7, 12]
        expectation = [True, True, False, False, False]
        ec = end_conditions.StateLengthBelow(6)
        for l, e in zip(lengths, expectation):
            self.assertEqual(e, ec(None, range(l)))

    def test_vary_condition(self):
        lengths     = [0, 5, 6, 7, 12]
        expectation = [False, False, False, True, True]
        state = range(6)
        for l, e in zip(lengths, expectation):
            ec = end_conditions.StateLengthBelow(l)
            self.assertEqual(e, ec(None, state))

if '__main__' == __name__:
    unittest.main()
