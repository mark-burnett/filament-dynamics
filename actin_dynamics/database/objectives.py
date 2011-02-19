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
from . import experiments as _experiments
from . import parameters as _parameters

class Objective(object):
    def __init__(self, analysis=None, configuration=None, value=None,
                 parameters=None):
        if analysis:
            self.analysis = analysis
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

class ObjectiveConfiguration(object):
    def __init__(self, name=None, experiment=None, objectives=None, bind=None):
        if name:
            self.name = name
        if experiment:
            self.experiment = experiment
        if objectives:
            self.objectives = objectives
        if bind:
            self.bind = bind

    def __repr__(self):
        return "%s(objectives=%s, configuration=%s, bind=%s)" % (
            self.__class__.__name__, self.objectives,
            self.configuration, self.bind)

_orm.mapper(ObjectiveConfiguration, _tables.objective_configuration_table,
            properties={
    'objectives': _orm.relationship(Objective, backref='configuration'),
    'experiment': _orm.relationship(_experiments.Experiment,
        backref='objective_configurations'),
    'bind': _orm.relationship(_binds.ObjectiveBind)})
