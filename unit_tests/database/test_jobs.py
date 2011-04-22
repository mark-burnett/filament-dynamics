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

class TestJob(DBTestCase):
    def test_run_relationship(self):
        p = database.ControllerProcess()
        m = database.Model()
        ps = database.ParameterSet(model=m)

        j = database.Job(parameter_set=ps, creator=p)

        self.db_session.add(j)
        self.db_session.commit()

        j2 = self.db_session.query(database.Job).first()
        self.assertEqual(j, j2)
        self.assertEqual(ps, j2.parameter_set)
        self.assertTrue(j2.parameter_set.id >= 1)


if '__main__' == __name__:
    unittest.main()
