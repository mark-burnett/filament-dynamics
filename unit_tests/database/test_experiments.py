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
    def test_filament_binds(self):
        e = database.Experiment('test expt name')

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        fb = database.FilamentBind(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.filaments.append(fb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(fb, e2.filaments[0])

    def test_measurement_binds(self):
        e = database.Experiment('test expt name')

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.MeasurementBind(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.measurements.append(cb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(cb, e2.measurements[0])

    def test_end_condition_binds(self):
        e = database.Experiment('test expt name')

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.EndConditionBind(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.end_conditions.append(cb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(cb, e2.end_conditions[0])

    def test_concentration_binds(self):
        e = database.Experiment('test expt name')

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.ConcentrationBind(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.concentrations.append(cb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(cb, e2.concentrations[0])

    def test_transition_binds(self):
        e = database.Experiment('test expt name')

        class_name = 'test_class_name'
        fixed_arguments = {'fixed a': 'literal 1'}
        variable_arguments = {'variable a': 'par name 1'}

        cb = database.TransitionBind(class_name=class_name,
                fixed_arguments=fixed_arguments,
                variable_arguments=variable_arguments)
        e.transitions.append(cb)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(cb, e2.transitions[0])

    def test_session_relationship(self):
        s = database.Session('test session name')

        e = database.Experiment('test expt name', session=s)

        self.db_session.add(e)
        self.db_session.commit()

        e2 = self.db_session.query(database.Experiment).first()
        self.assertEqual(e, e2)
        self.assertEqual(s, e2.session)
        self.assertTrue(e2.session.id >= 1)

    def test_parameters(self):
        test_data = {'par_name_1': 7.2,
                     'par_name_2': 61.3}

        e = database.Experiment('ses 1')

        e.parameters = test_data

        self.db_session.add(e)
        self.db_session.commit()

        del e

        e2 = self.db_session.query(database.Experiment).first()
        for par_name, value in test_data.iteritems():
            self.assertEqual(value, e2.parameters[par_name])


if '__main__' == __name__:
    unittest.main()
