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

    def test_measurements(self):
        times = range(5)
        values = [t**2 for t in times]
        errors = [0.1 * v for v in values]

        a = database.Analysis()
        a.measurement = times, values, errors

        for i, result in enumerate(a.results):
            self.assertEqual(times[i], result.abscissa)
            self.assertEqual(values[i], result.ordinate)
            self.assertEqual(errors[i], result.error)

        self.assertEqual((times, values, errors), a.measurement)


if '__main__' == __name__:
    unittest.main()
