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

class TestObjective(DBTestCase):
    def test_run_relationship(self):
        r = database.Run()
        r.experiment_id = 0
        r.model_id = 0

        o = database.Objective(run=r)
        o.objective_bind_id = 0

        self.db_session.add(o)
        self.db_session.commit()

        o2 = self.db_session.query(database.Objective).first()
        self.assertEqual(o, o2)
        self.assertEqual(r, o2.run)
        self.assertTrue(o2.run.id >= 1)

    def test_objective_bind_relationship(self):
        ob = database.ObjectiveBind(class_name='test')
        ob.experiment_id = 0

        o = database.Objective(bind=ob)
        o.run_id = 0

        self.db_session.add(o)
        self.db_session.commit()

        o2 = self.db_session.query(database.Objective).first()
        self.assertEqual(o, o2)

    def test_parameters(self):
        test_data = {'par_name_1': 7.2,
                     'par_name_2': 61.3}

        o = database.Objective()
        o.run_id = 0
        o.objective_bind_id = 0

        o.parameters = test_data

        self.db_session.add(o)
        self.db_session.commit()

        del o

        o2 = self.db_session.query(database.Objective).first()
        for par_name, value in test_data.iteritems():
            self.assertEqual(value, o2.parameters[par_name])


if '__main__' == __name__:
    unittest.main()
