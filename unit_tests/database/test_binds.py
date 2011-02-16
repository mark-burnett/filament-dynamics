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

engine = create_engine('sqlite:///:memory:')#, echo=True)
db_session = orm.scoped_session(orm.sessionmaker(bind=engine))

class TestBind(unittest.TestCase):
    def setUp(self):
        database.metadata.create_all(engine)

#    def tearDown(self):
#        database.metadata.drop_all(engine)

    def test_alive(self):
        self.assertEqual(0, db_session.query(database.Bind).count())

        b = database.Bind()
#        b.parameters['test arg a'] = 'test par 1'
#        b.fixed_parameters['fixed arg b'] = 'literal 1'
        b.module_name = 'filaments'
        b.class_name = 'test_class'

        db_session.add(b)
        db_session.commit()

        self.assertEqual(1, db_session.query(database.Bind).count())

#    def test_alive2(self):
#        self.assertEqual(0, db_session.query(database.Bind).count())

if '__main__' == __name__:
    unittest.main()
