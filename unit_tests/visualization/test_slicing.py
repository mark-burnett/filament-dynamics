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

import numpy
import itertools

from sqlalchemy import schema, types

from unit_tests.database import base_test_cases

from actin_dynamics import database
from actin_dynamics.visualization import slicing

class SlicerTests(base_test_cases.DBTestCase):
    def setUp(self):
        # Use parent class to setup test database.
        base_test_cases.DBTestCase.setUp(self)

        # Define table name and slice definition
        table_name = 'slice_test_table'
        self.slice_definition = database.SliceDefinition(table_name=table_name)
        self.slice_definition.objective_bind_id = 0

        # Build a slicing table.
        self.column_descriptions = {'parA': 'colA',
                                    'parB': 'colB'}

        self.table = self.build_slice_table(table_name,
                self.column_descriptions.values())
        # XXX bad news bind
        database.global_state.metadata.bind = self.engine

        # Populate Parameter Meshes
        meshA = range(10)
        meshB = [100 * a for a in meshA]
        self.meshes = {'parA': meshA, 'parB': meshB}
        self.populate_slice_meshes(self.slice_definition, self.meshes,
                                   self.column_descriptions)

        # Populate slice values
        self.populate_slice_values(self.table, self.meshes,
                                   self.column_descriptions)

#    def tearDown(self):
#        self.engine.drop(self.table)
#        self.table.drop()
#        database.global_state.metadata.bind = None
#        base_test_cases.DBTestCase.tearDown(self)

    def build_slice_table(self, table_name, col_names):
        columns = [schema.Column(cn, types.Float, index=True)
                   for cn in col_names]

        table = schema.Table(table_name, database.global_state.metadata,
                schema.Column('objective_id', types.Integer,
                              schema.ForeignKey('objective.id'), primary_key=True),
                schema.Column('value', types.Float, index=True),
                *columns)

        self.engine.create(table)
        return table

    def populate_slice_meshes(self, definition, meshes, column_names):
        with self.db_session.transaction:
            self.db_session.add(definition)
            for parameter_name, mesh in meshes.iteritems():
                sp = database.SliceParameter(parameter_name=parameter_name,
                        column_name=column_names[parameter_name],
                        definition=definition)
                sp.mesh = [database.SliceMesh(value=m) for m in mesh]

    def populate_slice_values(self, table, meshes, column_map):
        names = meshes.keys()
        mesh_values = meshes.values()
        for values in itertools.product(*mesh_values):
            dv = dict((n, v) for n, v in itertools.izip(names, values))
            cv = dict((column_map[n], v) for n, v in dv.iteritems())
            value = sum(values)
            cv['value'] = value
            cv['objective_id'] = value
            self.engine.execute(table.insert(cv))


    def test_everything(self):
        s = slicing.Slicer.from_slice_definition(self.slice_definition)
        self.assertEqual(0, s.get_best_value())

        # Minimum value tests.
        parA_mv_values, parA_mv_names, parA_mv_meshes = s.minimum_values('parA')
        self.assertEqual(range(10), list(parA_mv_values))
        self.assertEqual(['parA'], list(parA_mv_names))
        self.assertEqual([self.meshes['parA']], list(parA_mv_meshes))

        parB_mv_values, parB_mv_names, parB_mv_meshes = s.minimum_values('parB')
        self.assertEqual([i * 100 for i in xrange(10)],
                         list(parB_mv_values))
        self.assertEqual(['parB'], list(parB_mv_names))
        self.assertEqual([self.meshes['parB']], list(parB_mv_meshes))

        # Slicing tests.
        for slice_value in self.meshes['parB']:
            parA_s_values, parA_s_names, parA_s_meshes = s.slice(parB=slice_value)
            self.assertEqual([slice_value + v for v in self.meshes['parA']],
                             list(parA_s_values))
            self.assertEqual(['parA'], list(parA_s_names))
            self.assertEqual([self.meshes['parA']], list(parA_s_meshes))

        for slice_value in self.meshes['parA']:
            parB_s_values, parB_s_names, parB_s_meshes = s.slice(parA=slice_value)
            self.assertEqual([slice_value + v for v in self.meshes['parB']],
                             list(parB_s_values))
            self.assertEqual(['parB'], list(parB_s_names))
            self.assertEqual([self.meshes['parB']], list(parB_s_meshes))

        # Best parameter test.
        self.assertEqual({'parA': 0.0, 'parB': 0.0}, s.get_best_parameters())

        # Best value test.
        self.assertEqual(0.0, s.get_best_value())

        # Best id test.
        self.assertEqual(0, s.get_best_id())


if '__main__' == __name__:
    unittest.main()
