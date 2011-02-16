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
from . import binds as _binds
from . import parameters as _parameters


class Experiment(object):
    parameters = _ap('_parameters', 'value',
                     creator=_parameters.ExperimentParameter)

_orm.mapper(Experiment, _tables.experiment_table, properties={
    # XXX shouldn't I be linking to the analysis_configuration?
    'analyses': _orm.relationship(_binds.AnalysisBind,
        secondary=_tables.experiment_bind_table),

    # XXX likewise for objective configuration here?
    'objectives': _orm.relationship(_binds.ObjectiveBind,
        secondary=_tables.experiment_bind_table),

    'measurements': _orm.relationship(_binds.MeasurementBind,
        secondary=_tables.experiment_bind_table),
    'end_conditions': _orm.relationship(_binds.EndConditionBind,
        secondary=_tables.experiment_bind_table),
    'concentrations': _orm.relationship(_binds.ConcentrationBind,
        secondary=_tables.experiment_bind_table),
    'transitions': _orm.relationship(_binds.TransitionBind,
        secondary=_tables.experiment_bind_table),
    '_parameters': _orm.relationship(_parameters.ExperimentParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name'))})
