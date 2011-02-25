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

from sqlalchemy import create_engine, orm
from actin_dynamics import database

engine = create_engine('sqlite:///:memory:')
db_session = orm.scoped_session(orm.sessionmaker(bind=engine))

class TestRun(unittest.TestCase):
    def setUp(self):
        database.metadata.create_all(engine)

    def tearDown(self):
        database.metadata.drop_all(engine)

    def test_experiment_relationship(self):
        m = database.Model(name='test expt name')

        r = database.Run(experiment=m)

        db_session.add(r)
        db_session.commit()

        r2 = db_session.query(database.Run).first()
        self.assertEqual(r, r2)
        self.assertEqual(m, r2.model)
        self.assertTrue(r2.experiment.id >= 1)

    def test_experiment_relationship(self):
        e = database.Experiment(name='test expt name')

        r = database.Run(experiment=e)

        db_session.add(r)
        db_session.commit()

        r2 = db_session.query(database.Run).first()
        self.assertEqual(r, r2)
        self.assertEqual(e, r2.experiment)
        self.assertTrue(r2.experiment.id >= 1)

    def test_parameters(self):
        test_data = {'par_name_1': 7.2,
                     'par_name_2': 61.3}

        r = database.Run()

        r.parameters = test_data

        db_session.add(r)
        db_session.commit()

        del r

        r2 = db_session.query(database.Run).first()
        for par_name, value in test_data.iteritems():
            self.assertEqual(value, r2.parameters[par_name])

    def test_analysis_relationship(self):
        a = database.Analysis(name='test_name')
        r = database.Run(analysis_list=[a])
        a2 = database.Analysis(name='test_name2', run=r)
        a2.measurement = range(3), [2,1,3], [0.1, 1.2, 0.3]

        db_session.add(r)
        db_session.commit()

        r2 = db_session.query(database.Run).first()
        self.assertEqual(r, r2)

        self.assertEqual(a2.measurement, r2.analyses['test_name2'])
        self.assertTrue(r2.analysis_list[0].id >= 1)
        self.assertTrue(r2.analysis_list[1].id >= 1)

if '__main__' == __name__:
    unittest.main()
