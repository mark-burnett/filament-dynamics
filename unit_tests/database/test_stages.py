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

class TestExperiment(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)
        self.model = database.Model('test model')
        self.experiment = database.Experiment('test expt', model=self.model)

    def test_experiment_relationship(self):
        s = database.Stage(experiment=self.experiment)
        self.assertEqual(self.experiment.stages[0], s)

        s2 = database.Stage(experiment=self.experiment)
        self.assertEqual(self.experiment.stages[1], s2)

        self.db_session.add(self.experiment)
        self.db_session.commit()

        e = self.db_session.query(database.Experiment).first()
        self.assertEqual([s, s2], e.stages)

    def test_behavior_relationship(self):
        s = database.Stage(experiment=self.experiment)
        b = database.Behavior(stage=s)

        self.db_session.add(b)
        self.db_session.commit()

        b2 = self.db_session.query(database.Behavior).first()

        self.assertEqual(s, b2.stage)


if '__main__' == __name__:
    unittest.main()
