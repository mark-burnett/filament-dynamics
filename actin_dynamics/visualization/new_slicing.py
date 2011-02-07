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
import itertools
import operator

import numpy

from sqlalchemy import schema, types, orm, sql
import elixir

from actin_dynamics.io import database

class Slicer(object):
    def __init__(self, summary_class, table):
        self.summary_class = summary_class
        self.table         = table

    @classmethod
    def from_group(cls, group, value_name, value_type='run',
                   run_parameters=[], analysis_parameters=[]):
        '''
        value_type specifies whether to look in runs or analyses
                for the value name.
        value_type can either be 'run' or 'value'.
        '''
        table = _create_table(run_parameters=run_parameters,
                              analysis_parameters=analysis_parameters)
        column_names = run_parameters + analysis_parameters

        summary_class = _create_class(table, column_names)

        _fill_table(summary_class, group,
                    value_name=value_name, value_type=value_type,
                    run_parameters=run_parameters,
                    analysis_parameters=analysis_parameters)

        return cls(summary_class=summary_class, table=table)


    def _get_column(self, column_name):
        return getattr(self.summary_class, column_name)

    def _get_columns(self, column_names):
        return [self._get_column(name) for name in column_names]


    def _get_meshes(self, columns):
        results = []
        for column in columns:
            query = elixir.session.query(column).distinct().order_by(column)
            results.append(map(operator.itemgetter(0), query))
        return results


    def slice(self, **fixed_values):
        column_names = [c for c in self.summary_class.column_names
                        if c not in fixed_values]
        columns = self._get_columns(column_names)
        query = elixir.session.query(self.summary_class.value, *columns
                ).filter_by(**fixed_values)
        meshes = self._get_meshes(columns)

        values = _convert_results_to_array(query, meshes)
        return values, column_names, meshes


def _convert_results_to_array(query, meshes):
    shape = [len(m) for m in meshes]
    result = numpy.zeros(shape)

    for row in query:
        slices = []
        for i, abscissa_values in enumerate(meshes):
            index = bisect.bisect_left(abscissa_values, row[i + 1])
            slices.append(slice(index, index + 1))

        result[slices] = row[0] # Assign value.

    return result


# XXX Generate a meaningful unique id for the table
def _create_table(run_parameters, analysis_parameters, unique_id='temp'):
    columns = []
    for name in itertools.chain(run_parameters, analysis_parameters):
        columns.append(schema.Column(name, types.Float, index=True))

    table = schema.Table('slicing_%s' % unique_id, elixir.metadata,
                         schema.Column('id', types.Integer, primary_key=True),
                         schema.Column('run_id', types.Integer,
                                       schema.ForeignKey('run.id')),
                         schema.Column('value', types.Float),
                         prefixes=['TEMPORARY'],
                         *columns)
    elixir.metadata.create_all()

    return table

def _create_class(table, columns):
    class TempTable(object):
        column_names = columns
        def __init__(self, **kwargs):
            for key, value in kwargs.iteritems():
                setattr(self, key, value)

    orm.mapper(TempTable, table)

    return TempTable


def _fill_table(summary_class, group,
                value_name=None, value_type=None,
                run_parameters=None, analysis_parameters=None):
    if 'run' == value_type.lower():
        return _fill_run_table(summary_class, group,
                               value_name=value_name,
                               run_parameters=run_parameters)
    elif 'analysis' == value_type.lower():
        return _fill_analysis_table(summary_class, group,
                                    value_name=value_name,
                                    run_parameters=run_parameters,
                                    analysis_parameters=analysis_parameters)

def _fill_analysis_table(summary_class, group, value_name=None,
                         run_parameters=None, analysis_parameters=None):
    for run in database.Run.query.filter_by(group=group):
        run_properties = _extract_properties(run, run_parameters)
        for analysis in database.Analysis.query.filter_by(run=run):
            properties = _extract_properties(analysis, analysis_parameters,
                                             value_name=value_name)
            properties.update(run_properties)

            new_object = summary_class(**properties)
            new_object.run_id = run.id
            elixir.session.add(new_object)

    # XXX Be wary of burning through too much memory by not committing sooner.
    elixir.session.commit()

def _fill_run_table(summary_class, group, value_name, run_parameters):
    for run in database.Run.query.filter_by(group=group):
        run_properties = _extract_properties(run, run_parameters, value_name=value_name)
        new_object = summary_class(**run_properties)
        new_object.run_id = run.id
        elixir.session.add(new_object)

    # XXX Be wary of burning through too much memory by not committing sooner.
    elixir.session.commit()


def _extract_properties(obj, parameter_names, value_name=None):
    results = dict((name, obj.get_parameter(name))
                    for name in parameter_names)
    if value_name:
        results['value'] = obj.get_value(value_name)

    return results
