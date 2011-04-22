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

class TestRun(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)
        self.model = database.Model()
        self.parameter_set = database.ParameterSet(model=self.model)

        self.experiment = database.Experiment(model=self.model)

    def test_model_experiment_relationships(self):
        r = database.Run(experiment=self.experiment,
                parameter_set=self.parameter_set)

        self.db_session.add(r)
        self.db_session.commit()

        r2 = self.db_session.query(database.Run).first()
        self.assertEqual(r, r2)
        self.assertEqual(self.parameter_set, r2.parameter_set)
        self.assertEqual(self.experiment, r2.experiment)
        self.assertTrue(r2.experiment.id >= 1)

    def test_analyst_relationship(self):
        r = database.Run(experiment=self.experiment,
                parameter_set=self.parameter_set)

        ab1 = database.AnalystBinding(class_name='cls_name',
                label='test_label')
        ab2 = database.AnalystBinding(class_name='cls_name',
                label='diff_name')
        self.experiment.analysts.append(ab1)
        self.experiment.analysts.append(ab2)

        a1 = database.Analysis(binding=ab1, run=r)
        a2 = database.Analysis(binding=ab2, run=r)

        a2.value = range(3), [2,1,3], [0.1, 1.2, 0.3]

        self.db_session.add(r)
        self.db_session.commit()

        r2 = self.db_session.query(database.Run).first()
        self.assertEqual(r, r2)

        self.assertEqual(a2.value, r2.analyses[1].value)
        self.assertTrue(r2.analyses[0].id >= 1)
        self.assertTrue(r2.analyses[1].id >= 1)

if '__main__' == __name__:
    unittest.main()
