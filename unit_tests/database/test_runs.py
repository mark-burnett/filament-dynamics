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
        self.session = database.Session()

        self.model = database.Model(session=self.session)

        self.analysis_bind = database.AnalysisBind(class_name='cls_name',
                label='test_label')

        self.experiment = database.Experiment(session=self.session)
        self.experiment.analysis_list.append(self.analysis_bind)

    def test_model_experiment_relationships(self):
        r = database.Run(experiment=self.experiment, model=self.model)

        self.db_session.add(r)
        self.db_session.commit()

        r2 = self.db_session.query(database.Run).first()
        self.assertEqual(r, r2)
        self.assertEqual(self.model, r2.model)
        self.assertEqual(self.experiment, r2.experiment)
        self.assertTrue(r2.experiment.id >= 1)

    def test_parameters(self):
        test_data = {'par_name_1': 7.2,
                     'par_name_2': 61.3}

        r = database.Run(experiment=self.experiment, model=self.model)

        r.parameters = test_data

        self.db_session.add(r)
        self.db_session.commit()

        del r

        r2 = self.db_session.query(database.Run).first()
        for par_name, value in test_data.iteritems():
            self.assertEqual(value, r2.parameters[par_name])

    def test_analysis_relationship(self):
        r = database.Run(experiment=self.experiment, model=self.model)

        a = database.Analysis(name='test_name', bind=self.analysis_bind, run=r)

        a2 = database.Analysis(name='diff_name', bind=self.analysis_bind, run=r)

        a2.measurement = range(3), [2,1,3], [0.1, 1.2, 0.3]

        self.db_session.add(r)
        self.db_session.commit()

        r2 = self.db_session.query(database.Run).first()
        self.assertEqual(r, r2)

        self.assertEqual(a2.measurement, r2.analyses['diff_name'])
        self.assertTrue(r2.analysis_list[0].id >= 1)
        self.assertTrue(r2.analysis_list[1].id >= 1)

if '__main__' == __name__:
    unittest.main()
