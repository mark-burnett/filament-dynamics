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
from . import parameters as _parameters
from . import analyses as _analyses
from . import experiments as _experiments


class Run(object):
    def __init__(self, session=None, experiment=None, analyses=None,
                 parameters=None):
        if session:
            self.session = session
        if experiment:
            self.experiment = experiment
        if analyses:
            self.analyses = analyses
        if parameters:
            self.parameters = parameters

    def __repr__(self):
        return "%s(session=%s, experiment=%s, analyses=%s, parameters=%s)" % (
            self.__class__.__name__, self.session, self.experiment,
            self.analyses, self.parameters)

    parameters = _ap('_parameters', 'value',
                     creator=_parameters.RunParameter)

_orm.mapper(Run, _tables.run_table, properties={
    '_parameters': _orm.relationship(_parameters.RunParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    'analyses':   _orm.relationship(_analyses.Analysis, backref='run'),
    'experiment': _orm.relationship(_experiments.Experiment, backref='runs')})
