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


class ObjectiveDataEntry(object):
    def __init__(self, abscissa=None, ordinate=None):
        if abscissa:
            self.abscissa = abscissa
        if ordinate:
            self.ordinate = ordinate

    def __repr__(self):
        return "%s(abscissa=%s, ordinate=%s)" % (
            self.__class__.__name__, self.abscissa, self.ordinate)

_orm.mapper(ObjectiveDataEntry, _tables.objective_data_entry_table)


class ObjectiveData(object):
    def __init__(self, name=None, experiment=None):
        if name:
            self.name = name
        if experiment:
            self.experiment = experiment

    def __repr__(self):
        return "%s(name=%s, experiment=%s)" % (
            self.__class__.__name__, self.name, self.experiment)

_orm.mapper(ObjectiveData, _tables.objective_data_table, properties={
    'pairs': _orm.relationship(ObjectiveDataEntry)})


class Objective(object):
    def __init__(self, run=None, configuration=None, value=None,
                 parameters=None):
        if run:
            self.run = run
        if configuration:
            self.configuration = configuration
        if value:
            self.value = value
        if parameters:
            self.parameters = parameters

    def __repr__(self):
        return "%s(analysis=%s, value=%s, value=%s)" % (
            self.__class__.__name__, self.analysis,
            self.value, self.value)

    parameters = _ap('_parameters', 'value',
                     creator=_parameters.ObjectiveParameter)

_orm.mapper(Objective, _tables.objective_table, properties={
    '_parameters': _orm.relationship(_parameters.ObjectiveParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name'))})
