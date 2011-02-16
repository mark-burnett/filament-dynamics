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

class TestSession(unittest.TestCase):
    def setUp(self):
        database.metadata.create_all(engine)

    def tearDown(self):
        database.metadata.drop_all(engine)

    def test_parameters(self):
        test_data = {'par_name_1': 7.2,
                     'par_name_2': 61.3}

        s = database.Session('ses 1')

        s.parameters = test_data

        db_session.add(s)
        db_session.commit()

        del s

        s2 = db_session.query(database.Session).first()
        for par_name, value in test_data.iteritems():
            self.assertEqual(value, s2.parameters[par_name])


if '__main__' == __name__:
    unittest.main()
