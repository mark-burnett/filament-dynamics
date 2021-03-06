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
    def test_concentration_binds(self):
        m = database.Model('test model name')
        m.session_id = 0

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.ConcentrationBind(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        m.concentrations.append(cb)

        self.db_session.add(m)
        self.db_session.commit()

        m2 = self.db_session.query(database.Model).first()
        self.assertEqual(cb, m2.concentrations[0])

    def test_transition_binds(self):
        m = database.Model('test model name')
        m.session_id = 0

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.TransitionBind(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        m.transitions.append(cb)

        self.db_session.add(m)
        self.db_session.commit()

        m2 = self.db_session.query(database.Model).first()
        self.assertEqual(cb, m2.transitions[0])

    def test_session_relationship(self):
        s = database.Session('test session name')

        m = database.Model('test model name', session=s)

        self.db_session.add(m)
        self.db_session.commit()

        m2 = self.db_session.query(database.Model).first()
        self.assertEqual(m, m2)
        self.assertEqual(s, m2.session)
        self.assertTrue(m2.session.id >= 1)

if '__main__' == __name__:
    unittest.main()
