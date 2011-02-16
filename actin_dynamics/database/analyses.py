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
from sqlalchemy import sql as _sql
from sqlalchemy.ext.associationproxy import association_proxy as _ap

from . import tables as _tables
from . import binds as _binds
from . import experiments as _experiments
from . import parameters as _parameters
from . import results as _results

class Analysis(object):
    parameters = _ap('_parameters', 'value',
                     creator=_parameters.AnalysisParameter)

# Analysis should have binds
_orm.mapper(Analysis, _tables.analysis_table, properties={
    '_parameters': _orm.relationship(_parameters.AnalysisParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    'results': _orm.relationship(_results.AnalysisResult, backref='analysis')})

class AnalysisConfiguration(object):
    pass

_orm.mapper(AnalysisConfiguration, _tables.analysis_configuration_table, properties={
    'experiment': _orm.relationship(_experiments.Experiment),
    'bind': _orm.relationship(_binds.AnalysisBind),
    'analyses': _orm.relationship(Analysis, backref='configuration')})
