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

import datetime

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
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')


# ---------------------------------------------------------------------
# - Job control branch                                                -
# ---------------------------------------------------------------------
# The purpose of the process table is purely provenance.
process_table = schema.Table('process', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        # XXX Add something to identify what code path we're using?
        schema.Column('type', schema.types.String(MAX_POLY_LENGTH),
                      index=True),

        # These identify the code.
        schema.Column('code_revision', schema.types.Integer),
        schema.Column('code_changeset', schema.types.String(40)),

        # These identify the machine.
        # First, the hostname (not always identical to the below nodename).
        schema.Column('hostname', schema.types.String(MAX_NAME_LENGTH)),
        # These 5 columns come from `uname -a`.
        schema.Column('sysname',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('nodename', schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('release',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('version',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('machine',  schema.types.String(MAX_NAME_LENGTH)),

        # These identify the time.
        schema.Column('start_time', schema.types.DateTime,
            default=datetime.datetime.now),
        schema.Column('stop_time', schema.types.DateTime),
        mysql_engine='InnoDB')

job_table = schema.Table('job', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')),
        schema.Column('creator_id', schema.types.Integer,
                      schema.ForeignKey('process.id')),
        schema.Column('worker_id', schema.types.Integer,
                      schema.ForeignKey('process.id')),
        schema.Column('complete', schema.types.Boolean, index=True,
                      default=False),
        mysql_engine='InnoDB')


# ---------------------------------------------------------------------
# - Configuration branch                                              -
# ---------------------------------------------------------------------

# Parameters
parameters_table = schema.Table('parameter', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('value', schema.types.Float, index=True),
        schema.Column('type',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True),
        mysql_engine='InnoDB')

session_parameters_table = schema.Table('session_parameter',
                                        global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('session.id')),
        mysql_engine='InnoDB')

schema.Index('session_parameters_unique_columns',
             session_parameters_table.c.parameter_id,
             session_parameters_table.c.session_id,
             unique=True)

experiment_parameters_table = schema.Table('experiment_parameter',
                                           global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiment.id')),
        mysql_engine='InnoDB')

schema.Index('experiment_parameters_unique_columns',
             experiment_parameters_table.c.parameter_id,
             experiment_parameters_table.c.experiment_id,
             unique=True)

run_parameters_table = schema.Table('run_parameter',
                                    global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')),
        mysql_engine='InnoDB')

schema.Index('run_parameters_unique_columns',
             run_parameters_table.c.parameter_id,
             run_parameters_table.c.run_id,
             unique=True)

objective_parameters_table = schema.Table('objective_parameter',
                                          global_state.metadata,
        schema.Column('parameter_id', schema.types.Integer,
                      schema.ForeignKey('parameter.id'), primary_key=True),
        schema.Column('objective_id', schema.types.Integer,
                      schema.ForeignKey('objective.id')),
        mysql_engine='InnoDB')

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
                      nullable=False, index=True),
        mysql_engine='InnoDB')

schema.Index('argument_unique_columns',
             argument_table.c.bind_id,
             argument_table.c.name,
             unique=True)

fixed_argument_table = schema.Table('fixed_argument', global_state.metadata,
        schema.Column('argument_id', schema.types.Integer,
                      schema.ForeignKey('argument.id'), primary_key=True),
        schema.Column('value', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

variable_argument_table = schema.Table('variable_argument',
                                       global_state.metadata,
        schema.Column('argument_id', schema.types.Integer,
                      schema.ForeignKey('argument.id'), primary_key=True),
        # NOTE Technically this is a foreign key, but I never do any lookups
            # from here, so there's no need to include the index.
        schema.Column('parameter_name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')


# Bindings (map strings/yaml repr to object factories)
bind_table = schema.Table('bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('module_name',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False),
        schema.Column('class_name', schema.types.String(MAX_NAME_LENGTH),
                      nullable=False),
        schema.Column('label', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')


# Experiment definitions
experiment_table = schema.Table('experiment', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('session.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

schema.Index('experiment_unique_columns',
             experiment_table.c.session_id,
             experiment_table.c.name,
             unique=True)


# Connects simulation, analysis, & objective primitives to experiment.
experiment_bind_table = schema.Table('experiment_bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiment.id')),
        mysql_engine='InnoDB')

schema.Index('experiment_bind_unique_columns',
             experiment_bind_table.c.experiment_id,
             experiment_bind_table.c.bind_id,
             unique=True)


objective_data_table = schema.Table('objective_data_entry',
                                    global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('objective_bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('abscissa', schema.types.Float),
        schema.Column('ordinate', schema.types.Float),
        schema.Column('error',    schema.types.Float),
        mysql_engine='InnoDB')


# Model definitions
model_table = schema.Table('model', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.types.Integer,
                      schema.ForeignKey('session.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

# Connects simulation primitives to model.
model_bind_table = schema.Table('model_bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('model_id', schema.types.Integer,
                      schema.ForeignKey('model.id')),
        mysql_engine='InnoDB')


# ---------------------------------------------------------------------
# - Data branch                                                       -
# ---------------------------------------------------------------------
run_table = schema.Table('run', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('experiment_id', schema.types.Integer,
                      schema.ForeignKey('experiment.id')),
        mysql_engine='InnoDB')


analysis_table = schema.Table('analysis', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

schema.Index('analysis_unique_columns',
             analysis_table.c.run_id,
             analysis_table.c.name,
             unique=True)


analysis_results_table = schema.Table('analysis_result',
                                      global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('analysis_id', schema.types.Integer,
                      schema.ForeignKey('analysis.id')),
        schema.Column('abscissa', schema.types.Float),
        schema.Column('ordinate', schema.types.Float),
        schema.Column('error',    schema.types.Float),
        mysql_engine='InnoDB')


objective_table = schema.Table('objective', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.types.Integer,
                      schema.ForeignKey('run.id')),
        schema.Column('objective_bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id')),
        schema.Column('value', schema.types.Float, index=True),
        mysql_engine='InnoDB')

schema.Index('objective_unique_columns',
             objective_table.c.run_id,
             objective_table.c.objective_bind_id,
             unique=True)
