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

class TestAnalysis(DBTestCase):
    def test_run_relationship(self):
        m = database.Model()
        ps = database.ParameterSet(model=m)
        e = database.Experiment(model=m)
        r = database.Run(parameter_set=ps, experiment=e)

        ab = database.AnalystBinding(class_name='cls_name', label='lbl')
        e.analysts.append(ab)
        a = database.Analysis(run=r, binding=ab)

        self.db_session.add(a)
        self.db_session.commit()

        a2 = self.db_session.query(database.Analysis).first()
        self.assertEqual(a, a2)
        self.assertEqual(r, a2.run)
        self.assertTrue(a2.run.id >= 1)


if '__main__' == __name__:
    unittest.main()
