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

import copy

from sqlalchemy import schema, types, orm

import elixir

from actin_dynamics.io import database

class Slicer(object):
    def __init__(self, summary_class):
        self.summary_class = summary_class

    @classmethod
    def from_group(cls, group,
                   run_parameters=[], analysis_parameters=[],
                   run_values=[],     analysis_values=[]):
        table = _create_table(run_parameters=run_parameters,
                              analysis_parameters=analysis_parameters,
                              run_values=run_values,
                              analysis_values=analysis_values)

        summary_class = _create_class(table)

        if analysis_parameters or analysis_values:
            _fill_full_table(summary_class, group,
                             run_parameters, run_values,
                             analysis_parameters, analysis_values)
        else:
            _fill_run_only_table(summary_class, group,
                                 run_parameters, run_values)

        return cls(summary_class)


def _create_table(run_parameters, analysis_parameters,
                  run_values, analysis_values, unique_id='temp'):
    columns = []
    for name in itertools.chain(run_parameters, analysis_parameters):
        columns.append(schema.Column(name, types.Float, index=True))

    for name in itertools.chain(run_values, analysis_values):
        columns.append(schema.Column(name, types.Float))

    table = schema.table('slicing_%s' % unique_id, elixir.session.metadata,
                         schema.Column('id', types.Integer, primary_key=True),
                         schema.Column('run_id', types.Integer,
                                       schema.ForeignKey('run.id')),
                         prefixes=['TEMPORARY'],
                         *columns)
    elixir.session.metadata.create_all()

    return table

def _create_class(table):
    class TempTable(object):
        pass
        # XXX Make sqlalchemy clonable mixin
        #  it won't be needed here though...
#        @classmethod
#        def clone(cls, source):
#            properties = {}
#            mapper = orm.object_mapper(source)
#            for col in mapper.columns:
#                if col.primary_key or col.foreign_keys:
#                    continue
#                properties[col.name] = getattr(source, col.name)
#
#            return cls(**properties)

    orm.mapper(TempTable, table)

    return TempTable

def _fill_full_table(summary_class, group,
                     run_parameters, run_values,
                     analysis_parameters, analysis_values):
    for run in database.Run.query.filter_by(group=group):
        run_properties = _extract_properties(run, run_parameters, run_values)
        for analysis in database.Analysis.query.filter_by(run=run):
            properties = _extract_properties(analysis,
                                             analysis_parameters,
                                             analysis_values)
            properties.update(run_properties)
            new_object = summary_class(**properties)

    # XXX Be wary of burning through too much memory by not committing sooner.
    elixir.session.commit()

def _fill_run_only_table(summary_class, group, run_parameters, run_values):
    for run in database.Run.query.filter_by(group=group):
        run_properties = _extract_properties(run, run_parameters, run_values)
        new_object = summary_class(run_properties)

    # XXX Be wary of burning through too much memory by not committing sooner.
    elixir.session.commit()

def _extract_properties(obj, parameter_names, value_names):
    parameters = dict((name, obj.get_parameter(name))
                      for name in parameter_names)
    values     = dict((name, obj.get_value(name)) for name in value_names)

    parameters.update(values)
    return parameters
