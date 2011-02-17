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

class TestParameter(unittest.TestCase):
    def setUp(self):
        database.metadata.create_all(engine)

    def tearDown(self):
        database.metadata.drop_all(engine)

    def test_inheritance_for_cross_talk(self):
        s = database.SessionParameter(name='hi', value=0.3)

        db_session.add(s)
        db_session.commit()

        self.assertEqual(1, db_session.query(database.Parameter).count())

        self.assertEqual(1, db_session.query(database.SessionParameter).count())
        self.assertEqual(0, db_session.query(database.ExperimentParameter).count())
        self.assertEqual(0, db_session.query(database.ModelParameter).count())
        self.assertEqual(0, db_session.query(database.RunParameter).count())
        self.assertEqual(0, db_session.query(database.AnalysisBind).count())
        self.assertEqual(0, db_session.query(database.ObjectiveParameter).count())

        o = database.ObjectiveParameter(name='bye', value=7.6)
        db_session.add(o)
        db_session.commit()

        self.assertEqual(2, db_session.query(database.Parameter).count())

        self.assertEqual(1, db_session.query(database.SessionParameter).count())
        self.assertEqual(0, db_session.query(database.ExperimentParameter).count())
        self.assertEqual(0, db_session.query(database.ModelParameter).count())
        self.assertEqual(0, db_session.query(database.RunParameter).count())
        self.assertEqual(0, db_session.query(database.AnalysisBind).count())
        self.assertEqual(1, db_session.query(database.ObjectiveParameter).count())


if '__main__' == __name__:
    unittest.main()
