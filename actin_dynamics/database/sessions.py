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
from . import experiments as _experiments
from . import parameters as _parameters
from . import models as _models
from . import runs as _runs

class Session(object):
    def __repr__(self):
        return 'Session(id=%s, name="%s")' % (self.id, self.name)

    parameters = _ap('_parameters', 'value',
                     creator=_parameters.SessionParameter)


_orm.mapper(Session, _tables.session_table,
            properties={
    '_parameters': _orm.relationship(_parameters.SessionParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    'experiments': _orm.relationship(_experiments.Experiment,
                                     backref='session'),
    'models': _orm.relationship(_models.Model, backref='session'),
    'runs': _orm.relationship(_runs.Run, backref='session')})