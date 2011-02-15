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
from . import parameters as _parameters

class Bind(object):
    fixed_parameters = _ap('_fixed_parameters', 'value',
                           creator=_parameters.FixedBindParameter)
    parameters = _ap('_parameters', 'value', creator=_parameters.BindParameter)

_bind_join = _sql.join(_tables.bind_table, _tables.bind_module_name_table)

_orm.mapper(Bind, _bind_join, properties={
    'module_name': _bind_join.c.bind_module_names_name,
    'module_name_id': _bind_join.c.bind_module_names_id,
    '_fixed_parameters': _orm.relationship(_parameters.FixedBindParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    '_parameters': _orm.relationship(_parameters.BindParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name'))})
