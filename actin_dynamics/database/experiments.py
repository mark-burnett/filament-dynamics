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
from . import experimental_data
from . import runs
from . import stages as _stages
from . import tables

__all__ = ['Experiment']

class Experiment(object):
    def __init__(self, name=None, model=None, filament_factory=None,
                 analysts=None, discriminators=None, stages=None):
        if name:
            self.name = name
        if model:
            self.model = model
        if filament_factory:
            self.filament_factory = filament_factory

        if stages:
            self.stages = stages

        if analysts:
            self.analysts = analysts
        if discriminators:
            self.discriminators = discriminators

    def __repr__(self):
        return "%s(id=%s, name=%r, model_id=%s, stages=%s)" % (
               self.__class__.__name__, self.id, self.name, self.model_id,
               self.stages)

    data = _ap('_data', 'value', creator=experimental_data.Data)

orm.mapper(Experiment, tables.experiment_table, properties={
    'filament_factory': orm.relationship(bindings.FilamentFactoryBinding,
        secondary=tables.experiment_binding_table, uselist=False,
        backref=orm.backref('experiment', uselist=False),
        cascade='all,delete-orphan', single_parent=True),

    'analysts': orm.relationship(bindings.AnalystBinding,
        secondary=tables.experiment_binding_table,
        backref=orm.backref('experiment', uselist=False),
        cascade='all,delete-orphan', single_parent=True),
    'discriminators': orm.relationship(bindings.DiscriminatorBinding,
        secondary=tables.experiment_binding_table,
        backref=orm.backref('experiment', uselist=False),
        cascade='all,delete-orphan', single_parent=True),

    'stages': orm.relationship(_stages.Stage, backref='experiment',
        cascade='all,delete-orphan'),

    '_data': orm.relationship(experimental_data.Data,
        collection_class=orm.collections.attribute_mapped_collection('name')),

    'runs': orm.relationship(runs.Run, backref='experiment',
        cascade='all,delete-orphan', single_parent=True)})
