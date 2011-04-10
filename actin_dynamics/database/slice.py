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
from . import binds as _binds

class SliceMesh(object):
    def __init__(self, parameter=None, value=None):
        if parameter:
            self.parameter = parameter
        if value is not None:
            self.value = value

_orm.mapper(SliceMesh, _tables.slice_mesh_table)

class SliceParameter(object):
    def __init__(self, parameter_name=None, column_name=None, definition=None):
        if parameter_name:
            self.parameter_name = parameter_name
        if column_name:
            self.column_name = column_name
        if definition:
            self.slice_definition = definition

_orm.mapper(SliceParameter, _tables.slice_parameter_table, properties={
    'mesh': _orm.relationship(SliceMesh, backref='parameter',
        cascade='all,delete-orphan')})


class SliceDefinition(object):
    def __init__(self, objective_bind=None, table_name=None):
        if objective_bind:
            self.objective_bind = objective_bind
        if table_name:
            self.table_name = table_name

    @property
    def column_map(self):
        return dict((sp.parameter_name, sp.column_name)
                    for sp in self.parameters)

    @property
    def meshes(self):
        return dict((sp.parameter_name,
            # XXX This should be done in the select query.
                        sorted([m.value for m in sp.mesh]))
                    for sp in self.parameters)

    def get_parameter(self, name):
        for sp in self.parameters:
            if name == sp.parameter_name:
                return sp


_orm.mapper(SliceDefinition, _tables.slice_definition_table, properties={
    'parameters': _orm.relationship(SliceParameter, backref='slice_definition',
        cascade='all,delete-orphan'),
    'objective_bind': _orm.relationship(_binds.ObjectiveBind,
        backref='slice_definition', single_parent=True)})
