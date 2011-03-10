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

import bisect

import numpy

from sqlalchemy import func, schema, sql

from actin_dynamics import database

class Slicer(object):
    def __init__(self, table, meshes, column_map):
        self.table      = table
        self.meshes     = meshes
        self.column_map = column_map

    @classmethod
    def from_objective_bind(cls, objective_bind):
        # XXX again with the 0
        sd = objective_bind.slice_definition[0]

        table_name = sd.table_name
        column_map = sd.column_map
        meshes     = sd.meshes

        table = schema.Table(table_name, database.global_state.metadata,
                             autoload=True)

        return cls(table, meshes, column_map)

    def slice(self, **fixed_values):
        abscissae_names = [n for n in self.column_map.keys()
                           if n not in fixed_values]
        select_columns = [self.table.c[self.column_map[n]]
                          for n in abscissae_names]
        select_columns.append(self.table.c.value)

        nearest_values = self.get_nearest_values(**fixed_values)
        like_clauses = [self.table.c[self.column_map[n]].like(v)
                        for n, v in nearest_values.iteritems()]

        query = sql.select(select_columns, whereclause=sql.and_(*like_clauses))

        result_set = query.execute()

        return _format_result(result_set, abscissae_names, self.meshes)


    def minimum_values(self, *abscissae_names):
        # We want to select all the columns except the objective id.
        column_names = [self.column_map[an] for an in abscissae_names]
        group_columns = [self.table.c[cn] for cn in column_names]
        # And the minimum value
        select_columns = group_columns + [func.min(self.table.c.value)]

        query = sql.select(select_columns, group_by=group_columns)
        result_set = query.execute()

        return _format_result(result_set, abscissae_names, self.meshes)


    def get_best_near(self, **fixed_values):
        nearest_values = self.get_nearest_values(**fixed_values)


    def get_nearest_values(self, **fixed_values):
        result = {}
        for name, value in fixed_values.iteritems():
            mesh = self.meshes[name]
            i = bisect.bisect_left(mesh, value)
            if len(mesh) <= i:
                result[name] = mesh[-1]
            elif 0 == i:
                result[name] = mesh[0]
            else:
                result[name] = min(mesh[i], mesh[i - 1])
        return result

    def get_best_parameters(self):
        parameter_names = self.column_map.keys()
        column_names = [self.column_map[n] for n in parameter_names]
        select_columns = [self.table.c[n] for n in column_names]

        best_id = self.get_best_id()
        result_set = sql.select(select_columns,
                                self.table.c.objective_id == best_id,
                                limit=1).execute()
        row = result_set.fetchone()
        result = dict((n, v) for n, v in zip(parameter_names, row)) #, row[len(row)-1]
        return result

    def get_best_id(self):
        result_set = sql.select([self.table.c.objective_id], limit=1,
                                ).order_by(self.table.c.value).execute()
        return result_set.scalar()

    def get_worst_value(self):
        result_set = sql.select([func.max(self.table.c.value)]).execute()
        return result_set.scalar()


def _format_result(result_set, names, meshes):
    '''
    Converts the (x(1), x(2), ..., x(n), y) tuples of a result set
    into an n-dimensional numpy array.
    '''
    mesh_list = [meshes[n] for n in names]

    shape = map(len, mesh_list)
    result = -numpy.ones(shape)

    for indexes, value in _index_iterator(result_set, mesh_list):
        result[tuple(indexes)] = value

    return result, names, mesh_list


def _index_iterator(result_set, mesh_list):
    for row in result_set:
        indexes = []
        for i, m in enumerate(row[:-1]):
            indexes.append(bisect.bisect_left(mesh_list[i], m))
        value = row[len(row)-1]
        yield tuple(indexes), value
