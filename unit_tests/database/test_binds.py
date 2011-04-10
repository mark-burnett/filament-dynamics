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

class TestBind(DBTestCase):
    def test_inheritance_for_cross_talk(self):
        s = database.Session()
        c = database.ConcentrationBind(class_name='test_class')
        e = database.Experiment(session=s, concentrations=[c])

        self.db_session.add(c)
        self.db_session.commit()

        self.assertEqual(1, self.db_session.query(database.Bind).count())

        self.assertEqual(1, self.db_session.query(database.ConcentrationBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.TransitionBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.EndConditionBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.MeasurementBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.FilamentBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.AnalysisBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.ObjectiveBind
            ).count())

        f = database.FilamentBind(class_name='test_class_2')
        e.filaments.append(f)
        self.db_session.add(f)
        self.db_session.commit()

        self.assertEqual(2, self.db_session.query(database.Bind).count())

        self.assertEqual(1, self.db_session.query(database.ConcentrationBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.TransitionBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.EndConditionBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.MeasurementBind
            ).count())
        self.assertEqual(1, self.db_session.query(database.FilamentBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.AnalysisBind
            ).count())
        self.assertEqual(0, self.db_session.query(database.ObjectiveBind
            ).count())

    def test_fixed_arguments(self):
        test_data = {'test_arg_a': 'literal 1',
                     'test_arg_b': 3.2}

        s = database.Session()
        t = database.TransitionBind(class_name='trans_class')
        e = database.Experiment(session=s, transitions=[t])
        t.fixed_arguments = test_data

        self.db_session.add(t)
        self.db_session.commit()

        del t

        t2 = self.db_session.query(database.TransitionBind).first()
        for arg, literal in test_data.iteritems():
            self.assertEqual(str(literal), t2.fixed_arguments[arg])

    def test_variable_arguments(self):
        test_data = {'test_arg_a': 'par_name_1',
                     'test_arg_b': 'par_name_2'}

        s = database.Session()
        t = database.TransitionBind(class_name='trans_class')
        e = database.Experiment(session=s, transitions=[t])
        t.variable_arguments = test_data

        self.db_session.add(t)
        self.db_session.commit()

        del t

        t2 = self.db_session.query(database.TransitionBind).first()
        for arg, par_name in test_data.iteritems():
            self.assertEqual(par_name, t2.variable_arguments[arg])

def TestObjectiveBind(DBTestCase):
    def test_data(self):
        times = range(5)
        values = [t**2 for t in times]
        errors = [0.1 * v for v in values]

        ob = database.ObjectiveBind()
        a.measurement = times, values, errors

        for i, result in enumerate(a.results):
            self.assertEqual(times[i], result.abscissa)
            self.assertEqual(values[i], result.ordinate)
            self.assertEqual(errors[i], result.error)

        self.assertEqual((times, values, errors), a.measurement)


if '__main__' == __name__:
    unittest.main()
