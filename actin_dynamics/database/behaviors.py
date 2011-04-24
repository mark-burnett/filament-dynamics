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

from . import bindings
from . import tables

__all__ = ['Behavior']

class Behavior(object):
    def __init__(self, concentrations=None, end_conditions=None,
                 observers=None, transitions=None,
                 experiment=None, model=None, stage=None):
        if concentrations:
            self.concentrations = concentrations
        if end_conditions:
            self.end_conditions = end_conditions
        if observers:
            self.observers = observers
        if transitions:
            self.transitions = transitions

        if experiment:
            self.experiment = experiment
        if model:
            self.model = model
        if stage:
            self.stage = stage

    def __repr__(self):
        return ("%s(id=%s, concentrations=%r, end_conditions=%r, " +
                "observers=%r, transitions=%s)") % (
               self.__class__.__name__, self.id, self.concentrations,
               self.end_conditions, self.observers, self.transitions)

orm.mapper(Behavior, tables.behavior_table, properties={
    'concentrations': orm.relationship(bindings.ConcentrationBinding,
        secondary=tables.behavior_binding_table,
        cascade='all,delete-orphan', single_parent=True),

    'end_conditions': orm.relationship(bindings.EndConditionBinding,
        secondary=tables.behavior_binding_table,
        cascade='all,delete-orphan', single_parent=True),

    'observers': orm.relationship(bindings.ObserverBinding,
        secondary=tables.behavior_binding_table,
        cascade='all,delete-orphan', single_parent=True),

    'transitions': orm.relationship(bindings.TransitionBinding,
        secondary=tables.behavior_binding_table,
        cascade='all,delete-orphan', single_parent=True)})
