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

class TestBehavior(DBTestCase):
    def test_observer_bindings(self):
        b = database.Behavior()

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.ObserverBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        b.observers.append(cb)

        self.db_session.add(b)
        self.db_session.commit()

        b2 = self.db_session.query(database.Behavior).first()
        self.assertEqual(cb, b2.observers[0])

    def test_end_condition_bindings(self):
        b = database.Behavior()

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.EndConditionBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        b.end_conditions.append(cb)

        self.db_session.add(b)
        self.db_session.commit()

        b2 = self.db_session.query(database.Behavior).first()
        self.assertEqual(cb, b2.end_conditions[0])

    def test_concentration_bindings(self):
        b = database.Behavior()

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.ConcentrationBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        b.concentrations.append(cb)

        self.db_session.add(b)
        self.db_session.commit()

        b2 = self.db_session.query(database.Behavior).first()
        self.assertEqual(cb, b2.concentrations[0])

    def test_transition_bindings(self):
        b = database.Behavior()

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.TransitionBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        b.transitions.append(cb)

        self.db_session.add(b)
        self.db_session.commit()

        b2 = self.db_session.query(database.Behavior).first()
        self.assertEqual(cb, b2.transitions[0])


if '__main__' == __name__:
    unittest.main()
