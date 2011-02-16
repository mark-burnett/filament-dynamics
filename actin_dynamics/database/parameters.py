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

from . import tables as _tables

class Parameter(object):
    def __init__(self, name, value, type):
        self.name  = name
        self.value = value
        self.type  = type

    def __repr__(self):
        return '%s(name=%s, value=%s, type=%s)' % (
                self.__class__.__name__, self.name, self.value, self.type)

_orm.mapper(Parameter, _tables.parameters_table,
            polymorphic_on=_tables.parameters_table.c.type)


class SessionParameter(Parameter): pass

_orm.mapper(SessionParameter, _tables.session_parameters_table,
            inherits=Parameter, polymorphic_identity='session')

class ExperimentParameter(Parameter): pass

_orm.mapper(ExperimentParameter, _tables.experiment_parameters_table,
            inherits=Parameter, polymorphic_identity='experiment')

class ModelParameter(Parameter): pass

_orm.mapper(ModelParameter, _tables.model_parameters_table,
            inherits=Parameter, polymorphic_identity='model')

class RunParameter(Parameter): pass

_orm.mapper(RunParameter, _tables.run_parameters_table,
            inherits=Parameter, polymorphic_identity='run')

class AnalysisParameter(Parameter): pass

_orm.mapper(AnalysisParameter, _tables.analysis_parameters_table,
            inherits=Parameter, polymorphic_identity='analysis')

class ObjectiveParameter(Parameter): pass

_orm.mapper(ObjectiveParameter, _tables.objective_parameters_table,
            inherits=Parameter, polymorphic_identity='objective')
