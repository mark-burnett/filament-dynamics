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
MAX_POLY_LENGTH = 16

# The database is mostly hierarchical, so this file is organized by level.

# ---------------------------------------------------------------------
# - Level 0: misc/non-hierarchical                                    -
# ---------------------------------------------------------------------

# Parameters
parameters_table = schema.Table('parameters', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('value', schema.types.Float, index=True),
        schema.Column('type',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True))

session_parameters_table = schema.Table('session_parameters',
                                        global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameters.id'), primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('sessions.id')))

schema.Index('session_parameters_unique_columns',
             session_parameters_table.c.parameter_id,
             session_parameters_table.c.session_id,
             unique=True)

experiment_parameters_table = schema.Table('experiment_parameters',
                                           global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameters.id'), primary_key=True),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiments.id')))

schema.Index('experiment_parameters_unique_columns',
             experiment_parameters_table.c.parameter_id,
             experiment_parameters_table.c.experiment_id,
             unique=True)

model_parameters_table = schema.Table('model_parameters',
                                      global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameters.id'), primary_key=True),
        schema.Column('model_id', schema.types.Integer,
                      schema.ForeignKey('models.id')))

schema.Index('model_parameters_unique_columns',
             model_parameters_table.c.parameter_id,
             model_parameters_table.c.model_id,
             unique=True)

run_parameters_table = schema.Table('run_parameters',
                                    global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameters.id'), primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('runs.id')))

schema.Index('run_parameters_unique_columns',
             run_parameters_table.c.parameter_id,
             run_parameters_table.c.run_id,
             unique=True)

analysis_parameters_table = schema.Table('analysis_parameters',
                                         global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameters.id'), primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analyses.id')))

schema.Index('analysis_parameters_unique_columns',
             analysis_parameters_table.c.parameter_id,
             analysis_parameters_table.c.analysis_id,
             unique=True)

objective_parameters_table = schema.Table('objective_parameters',
                                          global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameters.id'), primary_key=True),
        schema.Column('objective_id', schema.types.Integer,
                      schema.ForeignKey('objectives.id')))

schema.Index('objective_parameters_unique_columns',
             objective_parameters_table.c.parameter_id,
             objective_parameters_table.c.objective_id,
             unique=True)

# Bind arguments
argument_table = schema.Table('arguments', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('binds.id')),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('type',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True))

schema.Index('argument_unique_columns',
             argument_table.c.bind_id,
             argument_table.c.name,
             unique=True)

fixed_argument_table = schema.Table('fixed_arguments', global_state.metadata,
        schema.Column('argument_id', schema.types.Integer,
                      schema.ForeignKey('arguments.id'), primary_key=True),
        schema.Column('value', schema.types.String(MAX_NAME_LENGTH)))

variable_argument_table = schema.Table('variable_arguments',
                                       global_state.metadata,
        schema.Column('argument_id', schema.types.Integer,
                      schema.ForeignKey('arguments.id'), primary_key=True),
        # NOTE Technically this is a foreign key, but I never do any lookups
            # from here, so there's no need to include the index.
        schema.Column('parameter_name', schema.types.String(MAX_NAME_LENGTH)))


# Job control
job_table = schema.Table('jobs', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('runs.id')),
        schema.Column('worker_uuid', schema.types.String(36), index=True),
        schema.Column('complete', schema.types.Boolean, index=True,
                      default=False))


# ---------------------------------------------------------------------
# - Level 1 (top level): session, experiments, & models               -
# ---------------------------------------------------------------------
session_table = schema.Table('sessions', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))


# Bindings (map strings/yaml repr to object factories)
bind_table = schema.Table('binds', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('module_name',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False),
        schema.Column('class_name', schema.types.String(MAX_NAME_LENGTH),
                      nullable=False))


# Experiment definitions
experiment_table = schema.Table('experiments', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('sessions.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

schema.Index('experiment_unique_columns',
             experiment_table.c.session_id,
             experiment_table.c.name,
             unique=True)

experiment_bind_table = schema.Table('experiment_binds', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('binds.id')),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiments.id')))


# Model definitions
model_table = schema.Table('models', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('sessions.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

model_bind_table = schema.Table('model_binds', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('binds.id')),
        schema.Column('model_id', schema.types.Integer,
                      schema.ForeignKey('models.id')))


# ---------------------------------------------------------------------
# - Level 2: run                                                      -
# ---------------------------------------------------------------------
run_table = schema.Table('runs', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('sessions.id')))


# ---------------------------------------------------------------------
# - Level 3: analysis                                                 -
# ---------------------------------------------------------------------
experiment_analysis_table = schema.Table('experiment_analyses',
                                         global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiments.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('binds.id')))

schema.Index('experiment_analysis_unique_columns',
             experiment_analysis_table.c.experiment_id,
             experiment_analysis_table.c.name,
             unique=True)


analysis_table = schema.Table('analyses', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('runs.id')),
        schema.Column('experiment_analysis_id', schema.types.Integer,
                      schema.ForeignKey('experiment_analyses.id')))

schema.Index('analysis_unique_columns',
             analysis_table.c.run_id,
             analysis_table.c.experiment_analysis_id,
             unique=True)


analysis_results_table = schema.Table('analysis_results',
                                      global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analyses.id')),
        schema.Column('abscissa', schema.types.Float),
        schema.Column('ordinate', schema.types.Float))


# ---------------------------------------------------------------------
# - Level 4: objective                                                -
# ---------------------------------------------------------------------
# XXX objectives must be in a given order per session!
        # This means experiments must also be in a given order per session.
    # I think we can just use the ordering the database gives us.
experiment_objective_table = schema.Table('experiment_objectives',
                                         global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiments.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('binds.id')))

schema.Index('experiment_objectives_unique_columns',
             experiment_objective_table.c.experiment_id,
             experiment_objective_table.c.name,
             unique=True)


objective_table = schema.Table('objectives', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analyses.id')),
        schema.Column('experiment_objective_id', schema.types.Integer,
                      schema.ForeignKey('experiment_objectives.id')),
        schema.Column('value', schema.types.Float, index=True))

schema.Index('objectives_unique_columns',
             objective_table.c.analysis_id,
             objective_table.c.experiment_objective_id,
             unique=True)
