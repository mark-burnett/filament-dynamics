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

class TestBind(unittest.TestCase):
    def setUp(self):
        database.metadata.create_all(engine)

    def tearDown(self):
        database.metadata.drop_all(engine)

    def test_inheritance_for_cross_talk(self):
        s = database.Session('ses 1')

#    def test_variable_arguments(self):
#        test_data = {'test_arg_a': 'par_name_1',
#                     'test_arg_b': 'par_name_2'}
#
#        t = database.TransitionBind('trans_class')
#        t.variable_arguments = test_data
#
#        db_session.add(t)
#        db_session.commit()
#
#        del t
#
#        t2 = db_session.query(database.TransitionBind).first()
#        for arg, par_name in test_data.iteritems():
#            self.assertEqual(par_name, t2.variable_arguments[arg])


if '__main__' == __name__:
    unittest.main()
