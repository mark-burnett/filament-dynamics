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

from . import tables
from . import bindings
from . import runs

__all__ = ['Experiment']

class Experiment(object):
    def __init__(self, name=None, model=None,
                 filaments=None, observers=None, end_conditions=None,
                 concentrations=None, transitions=None,
                 analysts=None, discriminators=None):
        if name:
            self.name = name
        if model:
            self.model = model
        if filaments:
            self.filaments = filaments
        if observers:
            self.observers = observers
        if end_conditions:
            self.end_conditions = end_conditions
        if concentrations:
            self.concentrations = concentrations
        if transitions:
            self.transitions = transitions

        if analysts:
            self.analysts = analysts
        if discriminators:
            self.discriminators = discriminators

    def __repr__(self):
        return "%s(id=%s, name=%r, model_id=%s)" % (
               self.__class__.__name__, self.id, self.name, self.model_id)

    data = _ap('_data', 'value', creator=data.Data)

orm.mapper(Experiment, tables.experiment_table, properties={
    'filaments': orm.relationship(bindings.FilamentBind,
        secondary=tables.experiment_binding_table,
        cascade='all,delete-orphan',
        single_parent=True),
    'end_conditions': orm.relationship(bindings.EndConditionBind,
        secondary=tables.experiment_bind_table,
        cascade='all,delete-orphan',
        single_parent=True),
    'concentrations': orm.relationship(bindings.ConcentrationBind,
        secondary=tables.experiment_bind_table,
        cascade='all,delete-orphan',
        single_parent=True),
    'transitions': orm.relationship(bindings.TransitionBind,
        secondary=tables.experiment_bind_table,
        cascade='all,delete-orphan',
        single_parent=True),

    'observers': orm.relationship(bindings.ObserverBinding,
        secondary=tables.experiment_bind_table,
        cascade='all,delete-orphan',
        single_parent=True),
    'analysts': orm.relationship(bindings.AnalystBinding,
        secondary=tables.experiment_bind_table,
        cascade='all,delete-orphan',
        single_parent=True),
    'discriminators': orm.relationship(bindings.DiscriminatorBinding,
        secondary=tables.experiment_bind_table,
        cascade='all,delete-orphan',
        single_parent=True),

    '_data': orm.relationship(data.Data,
        collection_class=orm.collections.attribute_mapped_collection('name'),

    'runs': orm.relationship(runs.Run, backref='experiment',
        cascade='all,delete-orphan', single_parent=True)})
