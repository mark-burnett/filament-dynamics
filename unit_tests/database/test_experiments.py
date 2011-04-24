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

    def test_filament_factory_relationship(self):
        e = database.Experiment('test expt name', model=self.model)

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        fb = database.FilamentBinding(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments,
                experiment=e)

        self.db_session.add(e)
        self.db_session.commit()

        fb = self.db_session.query(database.FilamentBinding).first()
        self.assertEqual(e, fb.experiment)

    def test_behavior_relationship(self):
        e = database.Experiment('test expt name', model=self.model)
        b = database.Behavior(experiment=e)

        self.db_session.add(b)
        self.db_session.commit()

        b2 = self.db_session.query(database.Behavior).first()

        self.assertEqual(e, b2.experiment)

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
