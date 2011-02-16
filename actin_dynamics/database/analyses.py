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
from . import parameters as _parameters
from . import results as _results

class Analysis(object):
    parameters = _ap('_parameters', 'value',
                     creator=_parameters.AnalysisParameter)

# XXX broken
_analysis_join = _sql.join(_tables.analysis_table, _tables.analysis_name_table)

# Analysis should have binds
_orm.mapper(Analysis, _analysis_join, properties={
    'name_id': _analysis_join.c.analysis_names_id,
    '_parameters': _orm.relationship(_parameters.AnalysisParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    'bind': _orm.relationship(_binds.Bind),
    'results': _orm.relationship(_results.AnalysisResult, backref='analysis',
        primaryjoin=_analysis_join.c.analyses_id ==
                    _tables.analysis_results_table.c.analysis_id)})
