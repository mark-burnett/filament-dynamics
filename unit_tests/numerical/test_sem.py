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

from actin_dynamics.numerical import sem

class SEMTest(unittest.TestCase):
    def setUp(self):
        self.test_data = [2, 1, 1, 2]

    def test_noscale_noadd(self):
        self.assertEqual((1.5, 0.25),
                sem.standard_error_of_mean(self.test_data))

    def test_scale_noadd(self):
        self.assertEqual((3, 0.5),
                sem.standard_error_of_mean(self.test_data,
                    scale_by=2))

    def test_scale_add(self):
        self.assertEqual((4, 0.5),
                sem.standard_error_of_mean(self.test_data,
                    scale_by=2, add=1))



if '__main__' == __name__:
    unittest.main()
