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

from . import tables as _tables
from . import binds as _binds
from . import parameters as _parameters


class Objective(object):
    def __init__(self, run=None, bind=None, value=None, parameters=None):
        if run:
            self.run = run
        if bind:
            self.bind = bind
        if value is not None:
            self.value = value
        if parameters:
            self.parameters = parameters

    def __repr__(self):
        return "%s(run=%s, bind=%s, value=%s, parameters=%s)" % (
            self.__class__.__name__, self.run, self.bind, self.value,
            self.parameters)

    parameters = _ap('_parameters', 'value',
                     creator=_parameters.ObjectiveParameter)

    @property
    def all_parameters(self):
        result = dict(self.parameters)
        result.update(self.run.all_parameters)
        return result


_orm.mapper(Objective, _tables.objective_table, properties={
    '_parameters': _orm.relationship(_parameters.ObjectiveParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    'bind': _orm.relationship(_binds.ObjectiveBind)})
