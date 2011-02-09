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

from sqlalchemy import schema, types, orm
import elixir

from actin_dynamics.io import database

class Slicer(object):
    def __init__(self, summary_class, table):
        self.summary_class = summary_class
        self.table         = table

    @classmethod
    def from_group(cls, group, value_name, value_type=None,
                   run_parameters=None, analysis_parameters=None,
                   table_name=None):
        '''
        value_type specifies whether to look in runs or analyses
                for the value name.
        value_type can either be 'run' or 'value'.
        '''
        if value_type is None:
            value_type = 'run'
        if run_parameters is None:
            run_parameters = []
        if analysis_parameters is None:
            analysis_parameters = []
        if table_name is None:
            table_name = 'slicing_temp'

        table = _create_table(run_parameters=run_parameters,
                              analysis_parameters=analysis_parameters,
                              table_name=table_name)
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

    def _get_mesh_dicts(self, column_names):
        columns = self._get_columns(column_names)
        values  = self._get_meshes(columns)

        return dict((n, v) for n, v in itertools.izip(column_names, values))


    def slice(self, **fixed_values):
        column_names = [c for c in self.summary_class.column_names
                        if c not in fixed_values]
        columns = self._get_columns(column_names)
        query = elixir.session.query(self.summary_class.value, *columns
                ).filter_by(**fixed_values)
        meshes = self._get_meshes(columns)

        values = _convert_results_to_array(query, meshes)
        return values, column_names, meshes


    def minimum_values(self, *abscissae_names):
        meshes = self._get_meshes(self._get_columns(abscissae_names))

        shape = [len(m) for m in meshes]
        if not shape:
            best = elixir.session.query(self.summary_class
                    ).order_by('value').first()
            return _format_result(best, self.table)
        result = numpy.zeros(shape)

        for indexes, mesh_point in _iterate_meshes(abscissae_names, meshes,
                                                   enum=True):
            best = elixir.session.query(self.summary_class.value
                    ).filter_by(**mesh_point).order_by('value').first()
            result[tuple(indexes)] = best[0]
        return result, abscissae_names, meshes


def _convert_results_to_array(query, meshes):
    shape = [len(m) for m in meshes]
    if sum(shape) == 0:
        return numpy.array([query.first()])
    result = numpy.zeros(shape)

    for row in query:
        slices = []
        for i, abscissa_values in enumerate(meshes):
            index = bisect.bisect_left(abscissa_values, row[i + 1])
            slices.append(slice(index, index + 1))

        result[slices] = row[0] # Assign value.

    return result


# XXX Generate a meaningful unique id for the table
def _create_table(run_parameters, analysis_parameters, table_name):
    columns = []
    for name in itertools.chain(run_parameters, analysis_parameters):
        columns.append(schema.Column(name, types.Float, index=True))

    table = schema.Table(table_name, elixir.metadata,
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
        if not analysis_parameters:
            return _fill_run_table(summary_class, group,
                                   value_name=value_name,
                                   run_parameters=run_parameters)
        else:
            raise RuntimeError("This shouldn't happen.")
    elif 'analysis' == value_type.lower():
        return _fill_analysis_table(summary_class, group,
                                    value_name=value_name,
                                    run_parameters=run_parameters,
                                    analysis_parameters=analysis_parameters)
    else:
        raise RuntimeError("Illegal value_type specified.")

def _fill_analysis_table(summary_class, group, value_name=None,
                         run_parameters=None, analysis_parameters=None):
    for run in database.Run.query.filter_by(group=group):
        run_properties = _extract_properties(run, run_parameters)

        analysis_query = database.Analysis.query.filter_by(run=run)
        meshes = _get_analysis_meshes(analysis_query, analysis_parameters)

        for analysis_values in _iterate_meshes(analysis_parameters, meshes):
            best_value = _analysis_min_value(analysis_query,
                                             analysis_values,
                                             value_name)

            properties = analysis_values
            properties.update(run_properties)
            properties['value'] = best_value

            new_object = summary_class(**properties)
            new_object.run_id = run.id
            elixir.session.add(new_object)

    # XXX Be wary of burning through too much memory by not committing sooner.
    elixir.session.commit()


# XXX There may be a way to speed this up with real queries.
#       It probably requires completely abandoning elixir...which I will do..
def _get_analysis_meshes(query, parameter_names):
    values = dict((n, set()) for n in parameter_names)
    for analysis in query:
        for name in parameter_names:
            values[name].add(analysis.get_parameter(name))
    return [values[n] for n in parameter_names]


def _iterate_meshes(names, meshes, enum=False):
    if enum:
        iterator = itertools.product(*map(enumerate, meshes))
        for ivals in iterator:
            indexes = map(operator.itemgetter(0), ivals)
            values  = map(operator.itemgetter(1), ivals)
            yield indexes, dict((n, v) for n, v in itertools.izip(names, values))
    else:
        for values in itertools.product(*meshes):
            yield dict((n, v) for n, v in itertools.izip(names, values))


def _analysis_min_value(analyses, analysis_values, value_name):
    best = None
    for a in analyses:
        if a.contains_parameters(analysis_values):
            this_value = a.get_value(value_name)
            if best is None or this_value < best:
                best = this_value

    return best


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

def _format_result(obj, table):
    names  = table.c.keys()[3:]
    values = [getattr(obj, name) for name in names]
    return [obj.value], names, values
