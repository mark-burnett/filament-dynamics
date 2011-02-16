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
from sqlalchemy.ext.associationproxy import association_proxy as _ap
from sqlalchemy import sql as _sql

from . import tables as _tables
from . import arguments as _arguments

class Bind(object):
    fixed_parameters = _ap('_fixed_parameters', 'value',
                           creator=_arguments.FixedArgument)
    parameters = _ap('_parameters', 'value', creator=_arguments.VariableArgument)

_orm.mapper(Bind, _tables.bind_table,
            polymorphic_on=_tables.bind_table.c.module_name, properties={
    '_fixed_parameters': _orm.relationship(_arguments.FixedArgument,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    '_parameters': _orm.relationship(_arguments.Argument,
        collection_class=_orm.collections.attribute_mapped_collection('name'))})

# XXX Need to enforce/validate module_name
        # This can probably be done by having an intermediate class.
class ConcentrationBind(Bind): pass

_orm.mapper(ConcentrationBind, _tables.bind_table, inherits=Bind,
            polymorphic_identity='concentrations')

class TransitionBind(Bind): pass

_orm.mapper(TransitionBind, _tables.bind_table, inherits=Bind,
            polymorphic_identity='transitions')

class EndConditionBind(Bind): pass

_orm.mapper(EndConditionBind, _tables.bind_table, inherits=Bind,
            polymorphic_identity='end_conditions')

class MeasurementBind(Bind): pass

_orm.mapper(MeasurementBind, _tables.bind_table, inherits=Bind,
            polymorphic_identity='measurements')

class FilamentBind(Bind): pass

_orm.mapper(FilamentBind, _tables.bind_table, inherits=Bind,
            polymorphic_identity='filaments')

class AnalysisBind(Bind): pass

_orm.mapper(AnalysisBind, _tables.bind_table, inherits=Bind,
            polymorphic_identity='analyses')

class ObjectiveBind(Bind): pass

_orm.mapper(ObjectiveBind, _tables.bind_table, inherits=Bind,
            polymorphic_identity='objectives')
