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

from actin_dynamics.simulation import explicit_measurements

class MockConcentration(object):
    def remove_monomer(self):
        pass

    def add_monomer(self):
        pass

class LengthTest(unittest.TestCase):
    def test_normal_use(self):
        times  = [1, 2, 3, 4]
        lengths = [3, 7, 8, 1]

        m = explicit_measurements.StrandLength()

        for t, l in zip(times, lengths):
            m.perform(t, range(l))

        self.assertEqual(len(times), len(m.data))
        
        for t, l, d in zip(times, lengths, m.data):
            self.assertEqual((t, l), d)

if '__main__' == __name__:
    unittest.main()
