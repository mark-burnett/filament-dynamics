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

from . import behaviors
from . import experiments
from . import parameter_sets
from . import tables

__all__ = ['Model']

class Model(object):
    def __init__(self, name=None, session=None, concentrations=None,
                 transitions=None):
        if name:
            self.name = name
        if concentrations:
            self.concentrations = concentrations
        if transitions:
            self.transitions = transitions

    def __repr__(self):
        return "%s(id=%s, name=%r)" % (
            self.__class__.__name__, self.id, self.name)

orm.mapper(Model, tables.model_table, properties={
    'parameter_sets': orm.relationship(parameter_sets.ParameterSet,
        backref='model',
        cascade='all,delete-orphan'),
    'behavior': orm.relationship(behaviors.Behavior,
        backref=orm.backref('model', uselist=False),
        cascade='all', single_parent=True),
    'experiments': orm.relationship(experiments.Experiment, backref='model',
        cascade='all,delete-orphan')})
