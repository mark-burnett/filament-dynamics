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

class TestParameterSet(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)
        self.model = database.Model('test model name')
        self.parameter_set = database.ParameterSet(model=self.model)

    def test_model_relationship(self):
        self.assertEqual(self.parameter_set, self.model.parameter_sets[0])

        self.db_session.add(self.parameter_set)
        self.db_session.commit()

        ps2 = self.db_session.query(database.ParameterSet).first()
        self.assertEqual(self.model, ps2.model)

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
