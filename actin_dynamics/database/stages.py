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

__all__ = ['Stage']

class Stage(object):
    def __init__(self, experiment=None):
        if experiment:
            self.experiment = experiment

    def __repr__(self):
        return "%s(id=%s, experiment_id=%s)" % (
               self.__class__.__name__, self.id, self.experiment_id)


orm.mapper(Stage, tables.stage_table, properties={
    'concentrations': orm.relationship(bindings.ConcentrationBinding,
        secondary=tables.stage_binding_table,
        backref=orm.backref('stage', uselist=False),
        cascade='all,delete-orphan', single_parent=True),

    'end_conditions': orm.relationship(bindings.EndConditionBinding,
        secondary=tables.stage_binding_table,
        backref=orm.backref('stage', uselist=False),
        cascade='all,delete-orphan', single_parent=True),

    'observers': orm.relationship(bindings.ObserverBinding,
        secondary=tables.stage_binding_table,
        backref=orm.backref('stage', uselist=False),
        cascade='all,delete-orphan', single_parent=True),

    'transitions': orm.relationship(bindings.TransitionBinding,
        secondary=tables.stage_binding_table,
        backref=orm.backref('stage', uselist=False),
        cascade='all,delete-orphan', single_parent=True)})
