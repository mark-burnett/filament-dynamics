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

import sqlalchemy

from actin_dynamics import database

from unit_tests.database.base_test_cases import DBTestCase

class TestParameter(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)

        self.model = database.Model()
        self.parameter_set = database.ParameterSet(model=self.model)

    def test_manual_creation(self):
        p1 = database.Parameter(name='hi', value=0.3,
                parameter_set=self.parameter_set)

        self.db_session.add(p1)
        self.db_session.commit()

        self.assertEqual(0.3, self.parameter_set.parameters['hi'])

    def test_duplicate_names(self):
        p1 = database.Parameter(name='hi', value=0.3,
                parameter_set=self.parameter_set)
        p2 = database.Parameter(name='hi', value=3.6,
                parameter_set=self.parameter_set)

        self.db_session.add(p1)
        self.db_session.add(p2)
        self.assertRaises(sqlalchemy.exceptions.IntegrityError,
                self.db_session.commit)

    def test_dict_interface_assignment(self):
        self.parameter_set.parameters['hi'] = 0.3
        self.db_session.commit()

        self.assertEqual(0.3, self.parameter_set.parameters['hi'])

    def test_dict_interface_reassignment(self):
        self.test_dict_interface_assignment()
        self.parameter_set.parameters['hi'] = 7.2
        self.db_session.commit()

        self.assertEqual(7.2, self.parameter_set.parameters['hi'])


if '__main__' == __name__:
    unittest.main()
