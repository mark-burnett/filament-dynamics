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
from . import objectives as _objectives


class Experiment(object):
    def __init__(self,  name=None, session=None, parameters=None,
                 filaments=None, measurements=None, end_conditions=None,
                 concentrations=None, transitions=None,
                 analysis_list=None, objective_list=None):
        if name:
            self.name = name
        if session:
            self.session = session
        if parameters:
            self.parameters = parameters

        if filaments:
            self.filaments = filaments
        if measurements:
            self.measurements = measurements
        if end_conditions:
            self.end_conditions = end_conditions
        if concentrations:
            self.concentrations = concentrations
        if transitions:
            self.transitions = transitions

        if analysis_list:
            self.analysis_list = analysis_list
        if objective_list:
            self.objective_list = objective_list

    def __repr__(self):
        return "%s(id=%s, name='%s', session_id=%s)" % (
               self.__class__.__name__, self.id, self.name, self.session_id)

    parameters = _ap('_parameters', 'value',
                     creator=_parameters.ExperimentParameter)

    @property
    def analyses(self):
        return dict((b.label, b) for b in self.analysis_list)

    @property
    def objectives(self):
        return dict((b.label, b) for b in self.objective_list)

    @property
    def all_parameters(self):
        result = dict(self.parameters)
        result.update(self.session.parameters)
        return result

_orm.mapper(Experiment, _tables.experiment_table, properties={
    'filaments': _orm.relationship(_binds.FilamentBind,
        secondary=_tables.experiment_bind_table,
        cascade='all,delete-orphan'),
    'measurements': _orm.relationship(_binds.MeasurementBind,
        secondary=_tables.experiment_bind_table,
        cascade='all,delete-orphan'),
    'end_conditions': _orm.relationship(_binds.EndConditionBind,
        secondary=_tables.experiment_bind_table,
        cascade='all,delete-orphan'),
    'concentrations': _orm.relationship(_binds.ConcentrationBind,
        secondary=_tables.experiment_bind_table,
        cascade='all,delete-orphan'),
    'transitions': _orm.relationship(_binds.TransitionBind,
        secondary=_tables.experiment_bind_table,
        cascade='all,delete-orphan'),

    'analysis_list': _orm.relationship(_binds.AnalysisBind,
        secondary=_tables.experiment_bind_table,
        cascade='all,delete-orphan'),
    'objective_list': _orm.relationship(_binds.ObjectiveBind,
        secondary=_tables.experiment_bind_table,
        cascade='all,delete-orphan'),

    '_parameters': _orm.relationship(_parameters.ExperimentParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name'),
        cascade='all,delete-orphan')})
