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

from sqlalchemy import orm
from sqlalchemy.ext.associationproxy import association_proxy as _ap

from . import bindings
from . import experiments
from . import parameter_sets
from . import parameters
from . import tables

__all__ = ['Model']

class Model(object):
    def __init__(self, name=None, session=None, concentrations=None,
                 transitions=None, fixed_parameters=None):
        if name:
            self.name = name
        if concentrations:
            self.concentrations = concentrations
        if transitions:
            self.transitions = transitions

        # Provide an empty parameter set by defualt.
        if fixed_parameters:
            self.fixed_parameters = fixed_parameters

    def __repr__(self):
        return "%s(id=%s, name=%r)" % (
            self.__class__.__name__, self.id, self.name)

    fixed_parameters = _ap('_fixed_parameters', 'value',
                           creator=parameters.FixedParameter)


orm.mapper(Model, tables.model_table, properties={
    'parameter_sets': orm.relationship(parameter_sets.ParameterSet,
        backref='model', cascade='all,delete-orphan'),
    'experiments': orm.relationship(experiments.Experiment,
        backref='model', cascade='all,delete-orphan'),

    'transitions': orm.relationship(bindings.TransitionBinding,
        secondary=tables.model_binding_table,
        backref=orm.backref('model', uselist=False),
        cascade='all,delete-orphan', single_parent=True),

    '_fixed_parameters': orm.relationship(parameters.FixedParameter,
        collection_class=orm.collections.attribute_mapped_collection('name'),
        backref='model', cascade='all,delete-orphan')})
