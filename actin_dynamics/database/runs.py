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
from . import objectives as _objectives
from . import models as _models
from . import experiments as _experiments


class Run(object):
    def __init__(self, model=None, experiment=None, analyses=None,
                 objectives=None, parameters=None, analysis_list=None):
        if model:
            self.model = model
        if experiment:
            self.experiment = experiment
        if analyses:
            self.analyses = analyses
        if objectives:
            self.objectives = objectives
        if parameters:
            self.parameters = parameters
        if analysis_list:
            self.analysis_list = analysis_list

    def __repr__(self):
        return "%s(id=%s, experiment_id=%s, model_id=%s, parameters=%s)" % (
            self.__class__.__name__, self.id, self.experiment_id, self.model_id,
            self.parameters)

    parameters = _ap('_parameters', 'value', creator=_parameters.RunParameter)
    analyses   = _ap('_analyses', 'measurement', creator=_analyses.Analysis)

    def get_objective(self, label):
        for o in self.objectives:
            if label == o.bind.label:
                return o.value

    @property
    def all_parameters(self):
        result = dict(self.parameters)
        result.update(self.experiment.all_parameters)
        return result

    def _combine_binds(self, name):
        return (getattr(self.experiment, name, []) +
                getattr(self.model, name, []))

    @property
    def filaments(self):
        return self._combine_binds('filaments')

    @property
    def transitions(self):
        return self._combine_binds('transitions')

    @property
    def concentrations(self):
        return self._combine_binds('concentrations')

    @property
    def end_conditions(self):
        return self._combine_binds('end_conditions')

    @property
    def measurements(self):
        return self._combine_binds('measurements')


_orm.mapper(Run, _tables.run_table, properties={
    '_parameters': _orm.relationship(_parameters.RunParameter,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    '_analyses':   _orm.relationship(_analyses.Analysis,
        collection_class=_orm.collections.attribute_mapped_collection(
            'name')),
    'analysis_list': _orm.relationship(_analyses.Analysis, backref='run'),
    'objectives': _orm.relationship(_objectives.Objective, backref='run'),
    'model': _orm.relationship(_models.Model, backref='runs'),
    'experiment': _orm.relationship(_experiments.Experiment, backref='runs')})
