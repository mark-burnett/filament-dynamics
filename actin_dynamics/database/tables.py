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
MAX_LOG_MESSAGE_SIZE = 1024


# ---------------------------------------------------------------------
# - Logging                                                           -
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
# - Job control                                                       -
# ---------------------------------------------------------------------
# The purpose of the process table is purely provenance.
process_table = schema.Table('process', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('type', schema.types.String(MAX_POLY_LENGTH),
                      index=True),

        # These identify the code.
        schema.Column('code_hash', schema.types.String(40)),
        schema.Column('code_modified', schema.types.DateTime),

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
        schema.Column('parameter_set_id', schema.ForeignKey('parameter_set.id'),
                      unique=True, nullable=False),
        schema.Column('creator_id', schema.ForeignKey('process.id'),
                      nullable=False),
        schema.Column('worker_id', schema.ForeignKey('process.id')),
        schema.Column('start_time', schema.types.DateTime, index=True),
        schema.Column('stop_time', schema.types.DateTime, index=True),
        mysql_engine='InnoDB')


# ---------------------------------------------------------------------
# - Parameter binding                                                 -
# ---------------------------------------------------------------------
binding_table = schema.Table('binding', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('module_name',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True),
        schema.Column('class_name', schema.types.String(MAX_NAME_LENGTH),
                      nullable=False),
        schema.Column('label', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

# Bind arguments
argument_table = schema.Table('argument', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('binding_id', schema.ForeignKey('binding.id'),
                      nullable=False),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('type',  schema.types.String(MAX_POLY_LENGTH),
                      nullable=False, index=True),
        mysql_engine='InnoDB')

schema.Index('argument_unique_columns',
             argument_table.c.binding_id,
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


# Connect bindings to configuration.
model_binding_table = schema.Table('model_binding', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('binding_id', schema.ForeignKey('binding.id'),
                      unique=True, nullable=False),
        schema.Column('model_id', schema.ForeignKey('model.id'),
                      nullable=False),
        mysql_engine='InnoDB')

schema.Index('model_binding_unique_columns',
             model_binding_table.c.model_id,
             model_binding_table.c.binding_id,
             unique=True)


experiment_binding_table = schema.Table('experiment_binding',
                                        global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('binding_id', schema.ForeignKey('binding.id'),
                      unique=True, nullable=False),
        schema.Column('experiment_id', schema.ForeignKey('experiment.id'),
                      nullable=False),
        mysql_engine='InnoDB')

schema.Index('experiment_binding_unique_columns',
             experiment_binding_table.c.experiment_id,
             experiment_binding_table.c.binding_id,
             unique=True)


# ---------------------------------------------------------------------
# - Configuration                                                     -
# ---------------------------------------------------------------------

# Model is the root of the tree
model_table = schema.Table('model', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')


experiment_table = schema.Table('experiment', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('model_id', schema.ForeignKey('model.id'),
                      nullable=False),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH)),
        mysql_engine='InnoDB')

schema.Index('experiment_unique_columns',
             experiment_table.c.model_id,
             experiment_table.c.name,
             unique=True)


data_table = schema.Table('data', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('experiment_id', schema.ForeignKey('experiment.id'),
                      nullable=False),
        schema.Column('name', schema.types.String(MAX_NAME_LENGTH),
                      nullable=False, index=True),
        schema.Column('value', schema.types.PickleType),
        mysql_engine='InnoDB')

schema.InnoDB('data_unique_columns',
              data_table.c.experiment_id,
              data_table.c.name,
              unique=True)


# ---------------------------------------------------------------------
# - Results                                                           -
# ---------------------------------------------------------------------
paramter_set_table = schema.Table('parameter_set', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('model_id', schema.ForeignKey('model.id'),
                      nullable=False),
        mysql_engine='InnoDB')


parameter_table = schema.Table('parameter', global_state.metadata,
        schema.Column('id',    schema.types.Integer, primary_key=True),
        schema.Column('parameter_set_id',
                      schema.ForeignKey('parameter_set.id'), nullable=False),
        schema.Column('name',  schema.types.String(MAX_NAME_LENGTH)),
        schema.Column('value', schema.types.Float),
        mysql_engine='InnoDB')


run_table = schema.Table('run', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('parameter_set_id',
                      schema.ForeignKey('parameter_set.id'), nullable=False),
        schema.Column('experiment_id', schema.ForeignKey('experiment.id'),
                      nullable=False),
        mysql_engine='InnoDB')


analysis_table = schema.Table('analysis', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.ForeignKey('run.id'), nullable=False),
        schema.Column('binding_id', schema.ForeignKey('binding.id')),
        schema.Column('value', schema.types.PickleType),
        mysql_engine='InnoDB')

schema.Index('analysis_unique_columns',
             analysis_table.c.run_id,
             analysis_table.c.binding_id,
             unique=True)


objective_table = schema.Table('objective', global_state.metadata,
        schema.Column('id', schema.types.Integer, primary_key=True),
        schema.Column('run_id', schema.ForeignKey('run.id'), nullable=False),
        schema.Column('binding_id', schema.ForeignKey('binding.id'),
                      nullable=False),
        schema.Column('value', schema.types.Float),
        mysql_engine='InnoDB')

schema.Index('objective_unique_columns',
             objective_table.c.run_id,
             objective_table.c.binding_id,
             unique=True)
