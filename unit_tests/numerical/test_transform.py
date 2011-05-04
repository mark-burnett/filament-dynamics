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

from actin_dynamics.numerical import transform

class KeyTransformTest(unittest.TestCase):
    def test_key_transform(self):
        test_data = [{'key 1': 1, 'key 2': 2},
                     {'key 1': 3, 'key 3': 4},
                     {'key 2': 5, 'key 1': 6}]
        expected_result = {'key 1': [1, 3, 6],
                           'key 2': [2, 5],
                           'key 3': [4]}
        self.assertEqual(expected_result, transform.key_transform(test_data))


if '__main__' == __name__:
    unittest.main()

