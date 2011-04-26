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

from actin_dynamics import database

from unit_tests.database.base_test_cases import DBTestCase

class TestModel(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)
        self.model = database.Model(name='test model')

    def test_fixed_parameters(self):
        test_values = {'parA': 1.2, 'parB': 3.6}
        self.model.fixed_parameters = test_values

        self.assertEqual(test_values, self.model.fixed_parameters)


if '__main__' == __name__:
    unittest.main()
