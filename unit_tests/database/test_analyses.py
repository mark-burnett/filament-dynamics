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

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        database.metadata.create_all(engine)

    def tearDown(self):
        database.metadata.drop_all(engine)

    def test_run_relationship(self):
        r = database.Run()

        a = database.Analysis(run=r)

        db_session.add(a)
        db_session.commit()

        a2 = db_session.query(database.Analysis).first()
        self.assertEqual(a, a2)
        self.assertEqual(r, a2.run)
        self.assertTrue(a2.run.id >= 1)

    def test_parameters(self):
        test_data = {'par_name_1': 7.2,
                     'par_name_2': 61.3}

        a = database.Analysis()

        a.parameters = test_data

        db_session.add(a)
        db_session.commit()

        del a

        a2 = db_session.query(database.Analysis).first()
        for par_name, value in test_data.iteritems():
            self.assertEqual(value, a2.parameters[par_name])

    def test_configuration_relationship(self):
        c = database.AnalysisConfiguration()
        a = database.Analysis(configuration=c)

        db_session.add(a)
        db_session.commit()

        a2 = db_session.query(database.Analysis).first()
        self.assertEqual(a, a2)
        self.assertEqual(c, a2.configuration)
        self.assertTrue(a2.configuration.id >= 1)


class TestAnalysisConfiguration(unittest.TestCase):
    def setUp(self):
        database.metadata.create_all(engine)

    def tearDown(self):
        database.metadata.drop_all(engine)

    def test_analysis_relationship(self):
        a = database.Analysis()
        c = database.AnalysisConfiguration(analyses=[a])

        db_session.add(c)
        db_session.commit()

        c2 = db_session.query(database.AnalysisConfiguration).first()
        self.assertEqual(c, c2)
        self.assertEqual(a, c2.analyses[0])
        self.assertTrue(c2.analyses[0].id >= 1)

    def test_experiment_relationship(self):
        e = database.Experiment()
        c = database.AnalysisConfiguration(experiment=e)

        db_session.add(c)
        db_session.commit()

        c2 = db_session.query(database.AnalysisConfiguration).first()
        self.assertEqual(c, c2)
        self.assertEqual(e, c2.experiment)
        self.assertTrue(c2.experiment.id >= 1)

    def test_bind(self):
        b = database.AnalysisBind(class_name='test ana bind')
        c = database.AnalysisConfiguration(bind=b)

        db_session.add(c)
        db_session.commit()

        c2 = db_session.query(database.AnalysisConfiguration).first()
        self.assertEqual(c, c2)
        self.assertEqual(b, c2.bind)
        self.assertTrue(c2.bind.id >= 1)


if '__main__' == __name__:
    unittest.main()
