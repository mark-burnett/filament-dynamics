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


# The database has 3 major branches:  job control, configuration, and data
# with session at the top of the whole hierarchy.


# ---------------------------------------------------------------------
# - Top of the hierarchy                                              -
# ---------------------------------------------------------------------
session_table = schema.Table('session', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))


# ---------------------------------------------------------------------
# - Job control branch                                                -
# ---------------------------------------------------------------------
job_table = schema.Table('job', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')),
        schema.Column('worker_uuid', schema.types.String(36), index=True),
        schema.Column('complete', schema.types.Boolean, index=True,
                      default=False))


# ---------------------------------------------------------------------
# - Configuration branch                                              -
# ---------------------------------------------------------------------

# Parameters
parameters_table = schema.Table('parameter', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('value', schema.types.Float, index=True),
        schema.Column('type',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True))

session_parameters_table = schema.Table('session_parameter',
                                        global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('session.id')))

schema.Index('session_parameters_unique_columns',
             session_parameters_table.c.parameter_id,
             session_parameters_table.c.session_id,
             unique=True)

experiment_parameters_table = schema.Table('experiment_parameter',
                                           global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiment.id')))

schema.Index('experiment_parameters_unique_columns',
             experiment_parameters_table.c.parameter_id,
             experiment_parameters_table.c.experiment_id,
             unique=True)

model_parameters_table = schema.Table('model_parameter',
                                      global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('model_id', schema.types.Integer,
                      schema.ForeignKey('model.id')))

schema.Index('model_parameters_unique_columns',
             model_parameters_table.c.parameter_id,
             model_parameters_table.c.model_id,
             unique=True)

run_parameters_table = schema.Table('run_parameter',
                                    global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')))

schema.Index('run_parameters_unique_columns',
             run_parameters_table.c.parameter_id,
             run_parameters_table.c.run_id,
             unique=True)

analysis_parameters_table = schema.Table('analysis_parameter',
                                         global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analysis.id')))

schema.Index('analysis_parameters_unique_columns',
             analysis_parameters_table.c.parameter_id,
             analysis_parameters_table.c.analysis_id,
             unique=True)

objective_parameters_table = schema.Table('objective_parameter',
                                          global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('objective_id', schema.types.Integer,
                      schema.ForeignKey('objective.id')))

schema.Index('objective_parameters_unique_columns',
             objective_parameters_table.c.parameter_id,
             objective_parameters_table.c.objective_id,
             unique=True)

# Bind arguments
argument_table = schema.Table('argument', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('type',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True))

schema.Index('argument_unique_columns',
             argument_table.c.bind_id,
             argument_table.c.name,
             unique=True)

fixed_argument_table = schema.Table('fixed_argument', global_state.metadata,
        schema.Column('argument_id', schema.types.Integer,
                      schema.ForeignKey('argument.id'), primary_key=True),
        schema.Column('value', schema.types.String(MAX_NAME_LENGTH)))

variable_argument_table = schema.Table('variable_argument',
                                       global_state.metadata,
        schema.Column('argument_id', schema.types.Integer,
                      schema.ForeignKey('argument.id'), primary_key=True),
        # NOTE Technically this is a foreign key, but I never do any lookups
            # from here, so there's no need to include the index.
        schema.Column('parameter_name', schema.types.String(MAX_NAME_LENGTH)))


# Bindings (map strings/yaml repr to object factories)
bind_table = schema.Table('bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('module_name',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False),
        schema.Column('class_name', schema.types.String(MAX_NAME_LENGTH),
                      nullable=False))


# Experiment definitions
experiment_table = schema.Table('experiment', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('session.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

schema.Index('experiment_unique_columns',
             experiment_table.c.session_id,
             experiment_table.c.name,
             unique=True)

experiment_bind_table = schema.Table('experiment_bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiment.id')))


# Model definitions
model_table = schema.Table('model', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('session.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)))

model_bind_table = schema.Table('model_bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('model_id', schema.types.Integer,
                      schema.ForeignKey('model.id')))


# ---------------------------------------------------------------------
# - Data branch                                                       -
# ---------------------------------------------------------------------
run_table = schema.Table('run', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('session.id')))


analysis_configuration_table = schema.Table('analysis_configuration',
                                            global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiment.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')))

schema.Index('analysis_configuration_unique_columns',
             analysis_configuration_table.c.experiment_id,
             analysis_configuration_table.c.name,
             unique=True)


analysis_table = schema.Table('analysis', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')),
        schema.Column('analysis_configuration_id', schema.types.Integer,
                      schema.ForeignKey('analysis_configuration.id')))

schema.Index('analysis_unique_columns',
             analysis_table.c.run_id,
             analysis_table.c.analysis_configuration_id,
             unique=True)


analysis_results_table = schema.Table('analysis_result',
                                      global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analysis.id')),
        schema.Column('abscissa', schema.types.Float),
        schema.Column('ordinate', schema.types.Float))


objective_configuration_table = schema.Table('objective_configuration',
                                         global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiment.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')))

schema.Index('objectives_configuration_unique_columns',
             objective_configuration_table.c.experiment_id,
             objective_configuration_table.c.name,
             unique=True)


objective_table = schema.Table('objective', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analysis.id')),
        schema.Column('objective_configuration_id', schema.types.Integer,
                      schema.ForeignKey('objective_configuration.id')),
        schema.Column('value', schema.types.Float, index=True))

schema.Index('objectives_unique_columns',
             objective_table.c.analysis_id,
             objective_table.c.objective_configuration_id,
             unique=True)
