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
MAX_TABLE_NAME_LENGTH  = 30
MAX_COLUMN_NAME_LENGTH = 30
MAX_LOG_MESSAGE_SIZE = 1024


# The database has 3 major branches:  job control, configuration, and data
# with session at the top of the whole hierarchy.
# There are also a few tables dedicated to logging the application.


# ---------------------------------------------------------------------
# - Summary tables                                                    -
# ---------------------------------------------------------------------
# These tables contain no unique information.  Just for convenience.

# This table maps objective_bind_id's to slice table names.
slice_definition_table = schema.Table('slice_definition', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
# XXX This should be the primary key, but sqla doesn't like it..
        schema.Column('objective_bind_id', schema.types.Integer,
                      schema.ForeignKey('bind.id'),
                      unique=True, nullable=False),
        schema.Column('table_name', schema.types.String(MAX_TABLE_NAME_LENGTH),
                      unique=True, nullable=False),
        mysql_engine='InnoDB')

# This table maps parameter names to column names
slice_parameter_table = schema.Table('slice_parameter', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('slice_definition_id', schema.types.Integer,
                      schema.ForeignKey('slice_definition.id'),
                      nullable=False),
        schema.Column('parameter_name', schema.types.String(MAX_NAME_LENGTH),
                      nullable=False),
        schema.Column('column_name',
                      schema.types.String(MAX_COLUMN_NAME_LENGTH),
                      unique=True, nullable=False),
        mysql_engine='InnoDB')

slice_mesh_table = schema.Table('slice_mesh', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('slice_parameter_id',
                      schema.ForeignKey('slice_parameter.id'), nullable=False),
        schema.Column('value', schema.types.Float),
        mysql_engine='InnoDB')

# ---------------------------------------------------------------------
# - Logging tables                                                    -
# ---------------------------------------------------------------------
logging_table = schema.Table('logging', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('process_id', schema.ForeignKey('process.id')),
        # Time stamp
        schema.Column('time', schema.types.DateTime,
                      default=datetime.datetime.now, index=True),
        # Logger name
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        # Full path to file
        schema.Column('pathname', schema.types.String(MAX_NAME_LENGTH)),
        # Name of originating function.
        schema.Column('funcName', schema.types.String(MAX_NAME_LENGTH)),
        # Line number of logging event.
        schema.Column('lineno', schema.types.Integer),
        # Logging level.
        schema.Column('levelno', schema.types.Integer, index=True),
        schema.Column('levelname', schema.types.String(MAX_POLY_LENGTH),
                      index=True),
        # User specified logging message.
        schema.Column('message', schema.types.String(MAX_LOG_MESSAGE_SIZE)),
        mysql_engine='InnoDB')

exception_table = schema.Table('exception', global_state.metadata,
        schema.Column('logging_id', schema.ForeignKey('logging.id'),
                      primary_key=True),
        schema.Column('type_name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('message', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

traceback_table = schema.Table('traceback', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('exception_id', schema.types.Integer,
                      schema.ForeignKey('exception.logging_id'),
                      nullable=False),
        schema.Column('filename', schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('lineno', schema.types.Integer),
        schema.Column('module', schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('line', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')


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
        schema.Column('type', schema.types.String(MAX_POLY_LENGTH),
                      index=True),

        # These identify the code.
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
        schema.Column('run_id', schema.ForeignKey('run.id'),
                      unique=True, nullable=False),
        schema.Column('creator_id', schema.ForeignKey('process.id'),
                      nullable=False),
        schema.Column('worker_id', schema.ForeignKey('process.id')),
        schema.Column('start_time', schema.types.DateTime, index=True),
        schema.Column('stop_time', schema.types.DateTime, index=True),
        mysql_engine='InnoDB')


# ---------------------------------------------------------------------
# - Configuration branch                                              -
# ---------------------------------------------------------------------

# Parameters
parameters_table = schema.Table('parameter', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('value', schema.types.Float),
        schema.Column('type',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True),
        mysql_engine='InnoDB')

session_parameters_table = schema.Table('session_parameter',
                                        global_state.metadata,
        schema.Column('parameter_id', schema.ForeignKey('parameter.id'),
                      primary_key=True),
        schema.Column('session_id', schema.ForeignKey('session.id'),
                      nullable=False),
        mysql_engine='InnoDB')

schema.Index('session_parameters_unique_columns',
             session_parameters_table.c.parameter_id,
             session_parameters_table.c.session_id,
             unique=True)

experiment_parameters_table = schema.Table('experiment_parameter',
                                           global_state.metadata,
        schema.Column('parameter_id', schema.ForeignKey('parameter.id'),
                      primary_key=True),
        schema.Column('experiment_id', schema.ForeignKey('experiment.id'),
                      nullable=False),
        mysql_engine='InnoDB')

schema.Index('experiment_parameters_unique_columns',
             experiment_parameters_table.c.parameter_id,
             experiment_parameters_table.c.experiment_id,
             unique=True)

run_parameters_table = schema.Table('run_parameter',
                                    global_state.metadata,
        schema.Column('parameter_id', schema.ForeignKey('parameter.id'),
                      primary_key=True),
        schema.Column('run_id', schema.ForeignKey('run.id'),
                      nullable=False),
        mysql_engine='InnoDB')

schema.Index('run_parameters_unique_columns',
             run_parameters_table.c.parameter_id,
             run_parameters_table.c.run_id,
             unique=True)

objective_parameters_table = schema.Table('objective_parameter',
                                          global_state.metadata,
        schema.Column('parameter_id', schema.ForeignKey('parameter.id'),
                      primary_key=True),
        schema.Column('objective_id', schema.ForeignKey('objective.id'),
                      nullable=False),
        mysql_engine='InnoDB')

schema.Index('objective_parameters_unique_columns',
             objective_parameters_table.c.parameter_id,
             objective_parameters_table.c.objective_id,
             unique=True)


# Bind arguments
argument_table = schema.Table('argument', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.ForeignKey('bind.id'), nullable=False),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('type',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True),
        mysql_engine='InnoDB')

schema.Index('argument_unique_columns',
             argument_table.c.bind_id,
             argument_table.c.name,
             unique=True)

fixed_argument_table = schema.Table('fixed_argument', global_state.metadata,
        schema.Column('argument_id', schema.ForeignKey('argument.id'),
                      primary_key=True),
        schema.Column('value', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

variable_argument_table = schema.Table('variable_argument',
                                       global_state.metadata,
        schema.Column('argument_id', schema.ForeignKey('argument.id'),
                      primary_key=True),
        # NOTE Technically this is a foreign key, but I never do any lookups
            # from here, so there's no need to include the index.
        schema.Column('parameter_name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')


# Bindings (map strings/yaml repr to object factories)
bind_table = schema.Table('bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('module_name',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True),
        schema.Column('class_name', schema.types.String(MAX_NAME_LENGTH),
                      nullable=False),
        schema.Column('label', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')


# Experiment definitions
experiment_table = schema.Table('experiment', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.ForeignKey('session.id'),
                      nullable=False),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

schema.Index('experiment_unique_columns',
             experiment_table.c.session_id,
             experiment_table.c.name,
             unique=True)


# Connects simulation, analysis, & objective primitives to experiment.
# XXX Consider using multi-table inheritance for binds..
#       It has the drawback that I would have double inheritance.
experiment_bind_table = schema.Table('experiment_bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.ForeignKey('bind.id'),
                      unique=True, nullable=False),
        schema.Column('experiment_id', schema.ForeignKey('experiment.id'),
                      nullable=False),
        mysql_engine='InnoDB')

schema.Index('experiment_bind_unique_columns',
             experiment_bind_table.c.experiment_id,
             experiment_bind_table.c.bind_id,
             unique=True)


objective_data_table = schema.Table('objective_data_entry',
                                    global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('objective_bind_id', schema.ForeignKey('bind.id'),
                      nullable=False),
        schema.Column('abscissa', schema.types.Float),
        schema.Column('ordinate', schema.types.Float),
        schema.Column('error',    schema.types.Float),
        mysql_engine='InnoDB')


# Model definitions
model_table = schema.Table('model', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('session_id', schema.ForeignKey('session.id'),
                      nullable=False),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

# Connects simulation primitives to model.
model_bind_table = schema.Table('model_bind', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('bind_id', schema.ForeignKey('bind.id'),
                      unique=True, nullable=False),
        schema.Column('model_id', schema.ForeignKey('model.id'),
                      nullable=False),
        mysql_engine='InnoDB')


# ---------------------------------------------------------------------
# - Data branch                                                       -
# ---------------------------------------------------------------------
run_table = schema.Table('run', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('model_id', schema.ForeignKey('model.id'),
                      nullable=False),
        schema.Column('experiment_id', schema.ForeignKey('experiment.id'),
                      nullable=False),
        mysql_engine='InnoDB')


analysis_table = schema.Table('analysis', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.ForeignKey('run.id'), nullable=False),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

schema.Index('analysis_unique_columns',
             analysis_table.c.run_id,
             analysis_table.c.name,
             unique=True)


analysis_results_table = schema.Table('analysis_result',
                                      global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('analysis_id', schema.ForeignKey('analysis.id'),
                      nullable=False),
        schema.Column('abscissa', schema.types.Float),
        schema.Column('ordinate', schema.types.Float),
        schema.Column('error',    schema.types.Float),
        mysql_engine='InnoDB')


objective_table = schema.Table('objective', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.ForeignKey('run.id'), nullable=False),
        schema.Column('objective_bind_id', schema.ForeignKey('bind.id'),
                      nullable=False),
        schema.Column('value', schema.types.Float),
        mysql_engine='InnoDB')
