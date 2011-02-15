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

from sqlalchemy import orm as _orm
from sqlalchemy import sql as _sql

from . import tables as _tables

class Parameter(object):
    def __init__(self, name, value):
        self.name  = name
        self.value = value

    def __repr__(self):
        return '%s(name=%s, value=%s, name_id=%i, value_id=%i)' % (
                self.name, self.value, self.name_id, self.value_id)

class SessionParameter(Parameter): pass

_session_parameter_join = _sql.join(_tables.parameter_name_table,
                                    _tables.session_parameters_table)

_orm.mapper(SessionParameter, _session_parameter_join, properties={
    'name_id':  _session_parameter_join.c.parameter_names_id,
    'value_id': _session_parameter_join.c.session_parameters_id})

class ExperimentParameter(Parameter): pass

_experiment_parameter_join = _sql.join(_tables.parameter_name_table,
                                _tables.experiment_parameters_table)

_orm.mapper(ExperimentParameter, _experiment_parameter_join, properties={
    'name_id':  _experiment_parameter_join.c.parameter_names_id,
    'value_id': _experiment_parameter_join.c.experiment_parameters_id})

class RunParameter(Parameter): pass

_run_parameter_join = _sql.join(_tables.parameter_name_table,
                                _tables.run_parameters_table)

_orm.mapper(RunParameter, _run_parameter_join, properties={
    'name_id':  _run_parameter_join.c.parameter_names_id,
    'value_id': _run_parameter_join.c.run_parameters_id})


class FixedBindParameter(Parameter): pass

_fixed_parameter_join = _sql.join(_tables.bind_fixed_parameters_table,
                                  _tables.bind_argument_name_table)

_orm.mapper(FixedBindParameter, _fixed_parameter_join, properties={
    'argument_name_id': _fixed_parameter_join.c.bind_argument_names_id})

class BindParameter(Parameter): pass

# XXX working here
_bind_parameter_join = _sql.join(_tables.bind_parameters_table,
                                 _tables.bind_argument_name_table)

_orm.mapper(BindParameter, _bind_parameter_join, properties={
            'name_id':  _bind_parameter_join.c.bind_argument_names_id,
            'value_id': _bind_parameter_join.c.bind_parameters_id})
