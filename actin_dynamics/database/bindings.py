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

import itertools as _itertools

from sqlalchemy import orm
from sqlalchemy.ext.associationproxy import association_proxy as _ap

from . import tables
from . import arguments
from . import objectives
from . import analyses


__all__ = ['AnalystBinding', 'ConcentrationBinding', 'DiscriminatorBinding',
           'EndConditionBinding', 'FilamentBinding', 'ObserverBinding',
           'TransitionBinding']


def _create_bind(key, value):
    value.label = key
    return value

class Binding(object):
    def __init__(self, label=None, class_name=None,
                 fixed_arguments=None, variable_arguments=None):
        if label:
            self.label = label
        if class_name:
            self.class_name = class_name
        if fixed_arguments:
            self.fixed_arguments = fixed_arguments
        if variable_arguments:
            self.variable_arguments = variable_arguments

    def __repr__(self):
        return ("%s(id=%s, label='%s', class_name='%s'," +
                " fixed_arguments=%s," +
                " variable_arguments=%s)") % (
                self.__class__.__name__, self.id, self.label, self.class_name,
                dict(self.fixed_arguments),
                dict(self.variable_arguments))

    fixed_arguments = _ap('_fixed_arguments', 'value',
                          creator=arguments.FixedArgument)
    variable_arguments = _ap('_variable_arguments', 'parameter_name',
                    creator=arguments.VariableArgument)

orm.mapper(Binding, tables.binding_table,
           polymorphic_on=tables.binding_table.c.module_name,
           properties={
    '_fixed_arguments': orm.relationship(arguments.FixedArgument,
        collection_class=orm.collections.attribute_mapped_collection('name'),
        cascade='all,delete-orphan'),
    '_variable_arguments': orm.relationship(arguments.VariableArgument,
        collection_class=orm.collections.attribute_mapped_collection('name'),
        cascade='all,delete-orphan')})


class AnalystBinding(Binding): pass
orm.mapper(AnalystBinding, inherits=Binding, properties={
        'results': orm.relationship(analyses.Analysis,
            backref='binding', cascade='all,delete-orphan')},
    polymorphic_identity='analyses')

class ConcentrationBinding(Binding): pass
orm.mapper(ConcentrationBinding, inherits=Binding,
           polymorphic_identity='concentrations')

class DiscriminatorBinding(Binding): pass
orm.mapper(DiscriminatorBinding, inherits=Binding, properties={
        'results': orm.relationship(objectives.Objective,
            backref='binding', cascade='all,delete-orphan')},
    polymorphic_identity='discriminators')

class EndConditionBinding(Binding): pass
orm.mapper(EndConditionBinding, inherits=Binding,
           polymorphic_identity='end_conditions')

class FilamentBinding(Binding): pass
orm.mapper(FilamentBinding, inherits=Binding, polymorphic_identity='filaments')

class ObserverBinding(Binding): pass
orm.mapper(ObserverBinding, inherits=Binding, polymorphic_identity='observers')

class TransitionBinding(Binding): pass
orm.mapper(TransitionBinding, inherits=Binding,
           polymorphic_identity='transitions')
