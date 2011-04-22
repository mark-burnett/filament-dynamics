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

class TestExperiment(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)
        self.model = database.Model('test model name')


    def test_filament_bindings(self):
        e = database.Experiment('test expt name', model=self.model)

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        fb = database.FilamentBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.filaments.append(fb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(fb, e2.filaments[0])

    def test_observer_bindings(self):
        e = database.Experiment('test expt name', model=self.model)

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.ObserverBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.observers.append(cb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(cb, e2.observers[0])

    def test_end_condition_bindings(self):
        e = database.Experiment('test expt name', model=self.model)

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.EndConditionBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.end_conditions.append(cb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(cb, e2.end_conditions[0])

    def test_concentration_bindings(self):
        e = database.Experiment('test expt name', model=self.model)

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.ConcentrationBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.concentrations.append(cb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(cb, e2.concentrations[0])

    def test_transition_bindings(self):
        e = database.Experiment('test expt name', model=self.model)

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.TransitionBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.transitions.append(cb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(cb, e2.transitions[0])

    def test_model_relationship(self):
        e = database.Experiment('test expt name', model=self.model)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(e, e2)
        self.assertEqual(self.model, e2.model)
        self.assertTrue(e2.model.id >= 1)


if '__main__' == __name__:
    unittest.main()
