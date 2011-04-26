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

class TestStage(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)
        self.model = database.Model('test model')
        self.experiment = database.Experiment('test expt', model=self.model)
        self.stage = database.Stage(experiment=self.experiment)

    def test_experiment_relationship(self):
        self.assertEqual(self.experiment.stages[0], self.stage)

        s2 = database.Stage(experiment=self.experiment)
        self.assertEqual(self.experiment.stages[1], s2)

        self.db_session.add(self.experiment)
        self.db_session.commit()

        e = self.db_session.query(database.Experiment).first()
        self.assertEqual([self.stage, s2], e.stages)

    def test_observer_bindings(self):
        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.ObserverBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        self.stage.observers.append(cb)

        self.db_session.add(cb)
        self.db_session.commit()

        s2 = self.db_session.query(database.Stage).first()
        self.assertEqual(cb, s2.observers[0])

    def test_end_condition_bindings(self):
        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.EndConditionBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        self.stage.end_conditions.append(cb)

        self.db_session.add(cb)
        self.db_session.commit()

        s2 = self.db_session.query(database.Stage).first()
        self.assertEqual(cb, s2.end_conditions[0])

    def test_concentration_bindings(self):
        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.ConcentrationBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        self.stage.concentrations.append(cb)

        self.db_session.add(cb)
        self.db_session.commit()

        s2 = self.db_session.query(database.Stage).first()
        self.assertEqual(cb, s2.concentrations[0])

    def test_transition_bindings(self):
        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.TransitionBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        self.stage.transitions.append(cb)

        self.db_session.add(cb)
        self.db_session.commit()

        s2 = self.db_session.query(database.Stage).first()
        self.assertEqual(cb, s2.transitions[0])


if '__main__' == __name__:
    unittest.main()
