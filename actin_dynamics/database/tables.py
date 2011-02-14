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

import sqlalchemy

from . import global_state

MAX_NAME_LENGTH = 128

# XXX add multiple column indexes
# The database is mostly hierarchical, so this file is organized by level.

# Level 0 (top level): collection
collection_table = sqlalchemy.table('collections', global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True))

parameter_name_table = sqlalchemy.table('parameter_names',
                                        global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('collection_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('collections.id')),
        sqlalchemy.Column('name', sqlalchemy.String(MAX_NAME_LENGTH)))

analysis_name_table = sqlalchemy.table('analysis_names',
                                       global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('collection_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('collections.id')),
        sqlalchemy.Column('name', sqlalchemy.String(MAX_NAME_LENGTH)))

objective_name_table = sqlalchemy.table('objective_names',
                                        global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('collection_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('collections.id')),
        sqlalchemy.Column('name', sqlalchemy.String(MAX_NAME_LENGTH)))


# Level 1: session
session_table = sqlalchemy.table('sessions', global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('collection_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('collections.id')))

session_parameters_table = sqlalchemy.table('session_parameters',
                                      global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('session_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('sessions.id')),
        sqlalchemy.Column('parameter_name_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('parameter_names.id')),
        sqlalchemy.Column('value', sqlalchemy.Float, index=True))

sqlalchemy.Index('session_parameters_unique_columns',
                 session_parameters_table.c.session_id,
                 session_parameters_table.c.parameter_name_id,
                 unique=True)


# Level 2: run
run_table = sqlalchemy.table('runs', global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('session_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('sessions.id')))


run_parameters_table = sqlalchemy.table('run_parameters',
                                   global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('run_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('run.id')),
        sqlalchemy.Column('parameter_name_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('parameter_names.id'))),
        sqlalchemy.Column('value', sqlalchemy.Float, index=True))

sqlalchemy.Index('run_parameters_unique_columns',
                 run_parameters_table.c.run_id,
                 run_parameters_table.c.parameter_name_id,
                 unique=True)


# Level 3: analysis
analysis_table = sqlalchemy.table('analyses', global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('run_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('run.id')),
        sqlalchemy.Column('analysis_name_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('analysis_names.id')))

sqlalchemy.Index('analysis_unique_columns',
                 analysis_table.c.run_id,
                 analysis_table.c.analysis_name_id,
                 unique=True)


analysis_parameters_table = sqlalchemy.table('analysis_parameters',
                                   global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('analysis_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('analyses.id')),
        sqlalchemy.Column('parameter_name_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('parameter_names.id'))),
        sqlalchemy.Column('value', sqlalchemy.Float, index=True))

sqlalchemy.Index('analysis_parameters_unique_columns',
                 analysis_parameters_table.c.analysis_id,
                 analysis_parameters_table.c.parameter_name_id,
                 unique=True)


analysis_results_table = sqlalchemy.table('analysis_results',
                                          global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('analysis_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('analyses.id')),
        sqlalchemy.Column('analysis_name_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('analysis_names.id'))),
        sqlalchemy.Column('abscissa', sqlalchemy.Float),
        sqlalchemy.Column('ordinate', sqlalchemy.Float))

sqlalchemy.Index('analysis_results_unique_columns',
                 analysis_results_table.c.analysis_id,
                 analysis_results_table.c.analysis_name_id,
                 unique=True)


# Level 4: objective
objective_table = sqlalchemy.table('objectives', global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('analysis_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('analyses.id')),
        sqlalchemy.Column('objective_name_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('objective_names.id')))

sqlalchemy.Index('objectives_unique_columns',
                 objective_table.c.analysis_id,
                 objective_table.c.objective_name_id,
                 unique=True)


objective_parameters_table = sqlalchemy.table('objective_parameters',
                                   global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('objective_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('objective.id')),
        sqlalchemy.Column('parameter_name_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('parameter_names.id'))),
        sqlalchemy.Column('value', sqlalchemy.Float, index=True))

sqlalchemy.Index('objective_parameters_unique_columns',
                 objective_parameters_table.c.objective_id,
                 objective_parameters_table.c.parameter_name_id,
                 unique=True)


objective_results_table = sqlalchemy.table('objective_results',
                                           global_state.metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('objective_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('objective.id')),
        sqlalchemy.Column('objective_name_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('objective_names.id'))),
        sqlalchemy.Column('value', sqlalchemy.Float, index=True))

sqlalchemy.Index('objective_results_unique_columns',
                 objective_results_table.c.objective_id,
                 objective_results_table.c.objective_name_id,
                 unique=True)
