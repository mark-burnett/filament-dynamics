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

from . import jobs
from . import parameters
from . import runs

__all__ = ['ParameterSet']

class ParameterSet(object):
    def __init__(self, model=None, parameters=None):
        if model:
            self.model = model
        if parameters:
            self.parameters = parameters

    def __repr__(self):
        return "%s(id=%s, model_id=%s)" % (
            self.__class__.__name__, self.id, self.model_id)

    parameters = _ap('_parameters', 'value', creator=parameters.Parameter)

orm.mapper(ParameterSet, tables.parameter_set_table, properties={
    '_parameters': orm.relationship(parameters.Parameter,
        backref='parameter_set',
        collection_class=orm.collections.attribute_mapped_collection('name')),
    'run': orm.relationship(runs.Run, backref='parameter_set',
                            cascade='all,delete-orphan'),
    'job': orm.relationship(jobs.Job, backref='parameter_set',
                            cascade='all,delete-orphan')})
