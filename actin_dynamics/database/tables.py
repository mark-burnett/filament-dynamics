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

from sqlalchemy import schema

from . import global_state

MAX_NAME_LENGTH = 128

# The database is mostly hierarchical, so this file is organized by level.

# ---------------------------------------------------------------------
# - Level 1 (top level): session                                      -
# ---------------------------------------------------------------------
session_table = schema.Table('sessions', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

# Names
parameter_name_table = schema.Table('parameter_names', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH),
                          index=True))

analysis_name_table = schema.Table('analysis_names', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

objective_name_table = schema.Table('objective_names', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

# Parameters
session_parameters_table = schema.Table('session_parameters',
                                        global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('sessions.id')),
        schema.Column('parameter_name_id', schema.types.Integer,
                      schema.ForeignKey('parameter_names.id')),
        schema.Column('value', schema.types.Float, index=True))

schema.Index('session_parameters_unique_columns',
             session_parameters_table.c.session_id,
             session_parameters_table.c.parameter_name_id,
             unique=True)


# Bindings (map strings/yaml repr to object factories)
bind_module_name_table = schema.Table('bind_module_names',
                                      global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)))

bind_table = schema.Table('binds', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_module_name_id', schema.types.Integer,
                      schema.ForeignKey('bind_module_names.id')),
        schema.Column('class_name', schema.types.String(MAX_NAME_LENGTH)))

bind_argument_name_table = schema.Table('bind_argument_names',
                                        global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)))

bind_fixed_parameters_table = schema.Table('bind_fixed_parameters',
                                           global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('binds.id')),
        schema.Column('argument_id', schema.types.Integer,
                      schema.ForeignKey('bind_argument_names.id')),
        schema.Column('value', schema.types.String(MAX_NAME_LENGTH)))

bind_parameters_table = schema.Table('bind_parameters', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('binds.id')),
        schema.Column('argument_id', schema.types.Integer,
                      schema.ForeignKey('bind_argument_names.id')),
        schema.Column('parameter_name_id', schema.types.Integer,
                      schema.ForeignKey('parameter_names.id')))

schema.Index('bind_parameters_unique_columns',
             bind_parameters_table.c.bind_id,
             bind_parameters_table.c.parameter_name_id,
             unique=True)


# Experiment definitions
experiment_table = schema.Table('experiments', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('sessions.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

experiment_bind_table = schema.Table('experiment_binds', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiment.id')))


# Model definitions
model_table = schema.Table('models', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('sessions.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

model_bind_table = schema.Table('model_binds', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('model_id', schema.types.Integer,
                      schema.ForeignKey('model.id')))


# ---------------------------------------------------------------------
# - Level 2: run                                                      -
# ---------------------------------------------------------------------
run_table = schema.Table('runs', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('sessions.id')))


run_parameters_table = schema.Table('run_parameters',
                                    global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')),
        schema.Column('parameter_name_id', schema.types.Integer,
                      schema.ForeignKey('parameter_names.id')),
        schema.Column('value', schema.types.Float, index=True))

schema.Index('run_parameters_unique_columns',
             run_parameters_table.c.run_id,
             run_parameters_table.c.parameter_name_id,
             unique=True)


# ---------------------------------------------------------------------
# - Level 3: analysis                                                 -
# ---------------------------------------------------------------------
analysis_table = schema.Table('analyses', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')),
        schema.Column('analysis_name_id', schema.types.Integer,
                      schema.ForeignKey('analysis_names.id')))

schema.Index('analysis_unique_columns',
             analysis_table.c.run_id,
             analysis_table.c.analysis_name_id,
             unique=True)


analysis_results_table = schema.Table('analysis_results',
                                      global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analyses.id')),
        schema.Column('analysis_name_id', schema.types.Integer,
                      schema.ForeignKey('analysis_names.id')),
        schema.Column('abscissa', schema.types.Float),
        schema.Column('ordinate', schema.types.Float))

schema.Index('analysis_results_unique_columns',
             analysis_results_table.c.analysis_id,
             analysis_results_table.c.analysis_name_id,
             unique=True)


# ---------------------------------------------------------------------
# - Level 4: objective                                                -
# ---------------------------------------------------------------------
objective_table = schema.Table('objectives', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analyses.id')),
        schema.Column('objective_name_id', schema.types.Integer,
                      schema.ForeignKey('objective_names.id')))

schema.Index('objectives_unique_columns',
             objective_table.c.analysis_id,
             objective_table.c.objective_name_id,
             unique=True)


objective_parameters_table = schema.Table('objective_parameters',
                                          global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('objective_id', schema.types.Integer,
                      schema.ForeignKey('objective.id')),
        schema.Column('parameter_name_id', schema.types.Integer,
                      schema.ForeignKey('parameter_names.id')),
        schema.Column('value', schema.types.Float, index=True))

schema.Index('objective_parameters_unique_columns',
             objective_parameters_table.c.objective_id,
             objective_parameters_table.c.parameter_name_id,
             unique=True)


objective_results_table = schema.Table('objective_results',
                                       global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('objective_id', schema.types.Integer,
                      schema.ForeignKey('objective.id')),
        schema.Column('objective_name_id', schema.types.Integer,
                      schema.ForeignKey('objective_names.id')),
        schema.Column('value', schema.types.Float, index=True))

schema.Index('objective_results_unique_columns',
             objective_results_table.c.objective_id,
             objective_results_table.c.objective_name_id,
             unique=True)
