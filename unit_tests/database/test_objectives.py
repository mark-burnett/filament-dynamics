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
    def setUp(self):
        DBTestCase.setUp(self)
        self.model = database.Model()
        self.parameter_set = database.ParameterSet(model=self.model)

        self.experiment = database.Experiment(model=self.model)
        self.discriminator_binding = (
                database.DiscriminatorBinding(label='discriminator_label',
                    class_name='test class name', experiment=self.experiment))
        self.objective = database.Objective(
                parameter_set=self.parameter_set,
                binding=self.discriminator_binding)

        self.db_session.add(self.model)
        self.db_session.commit()

    def test_binding_relationship(self):
        self.assertTrue(False)

    def test_parameter_set_relationship(self):
        o = self.db_session.query(database.Objective).first()
        self.assertEqual(o.parameter_set, self.parameter_set)
