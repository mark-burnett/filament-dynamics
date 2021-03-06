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

class TestParameter(DBTestCase):
    def test_inheritance_for_cross_talk(self):
        s = database.SessionParameter(name='hi', value=0.3)
        s.session_id = 0

        self.db_session.add(s)
        self.db_session.commit()

        self.assertEqual(1, self.db_session.query(database.Parameter
            ).count())

        self.assertEqual(1, self.db_session.query(database.SessionParameter
            ).count())
        self.assertEqual(0, self.db_session.query(database.ExperimentParameter
            ).count())
        self.assertEqual(0, self.db_session.query(database.RunParameter
            ).count())
        self.assertEqual(0, self.db_session.query(database.ObjectiveParameter
            ).count())

        o = database.ObjectiveParameter(name='bye', value=7.6)
        o.objective_id = 0
        self.db_session.add(o)
        self.db_session.commit()

        self.assertEqual(2, self.db_session.query(database.Parameter
            ).count())

        self.assertEqual(1, self.db_session.query(database.SessionParameter
            ).count())
        self.assertEqual(0, self.db_session.query(database.ExperimentParameter
            ).count())
        self.assertEqual(0, self.db_session.query(database.RunParameter
            ).count())
        self.assertEqual(1, self.db_session.query(database.ObjectiveParameter
            ).count())

    def test_repeated_name_assignment(self):
        sp = database.SessionParameter(name='hi', value=0.3)
        sp.session_id = 0

        self.db_session.add(sp)
        self.db_session.commit()

        rp = database.RunParameter(name='hi', value=2.6)
        rp.run_id = 0

        self.db_session.add(rp)
        self.db_session.commit()


if '__main__' == __name__:
    unittest.main()
