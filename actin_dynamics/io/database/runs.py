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

import elixir as _elixir

from . import mixins as _mixins
from . import parameters as _parameters
from . import measurements as _measurements

class Run(_elixir.Entity, _mixins.GetOrCreate, _mixins.HasParameters):
    _elixir.using_options(tablename='run')

    parameters   = _elixir.OneToMany('SimulationParameter',
                                     cascade='all,delete,delete-orphan')
    measurements = _elixir.OneToMany('Measurement',
                                     cascade='all,delete,delete-orphan')

    analyses = _elixir.OneToMany('Analysis',
                                 cascade='all,delete,delete-orphan')
    values   = _elixir.OneToMany('SimulationValue',
                                 cascade='all,delete,delete-orphan')

    group = _elixir.ManyToOne('Group')

    @classmethod
    def from_analyzed_set(cls, analyzed_set):
        run = cls()
        run.parameters = _parameters.SimulationParameter.from_dict(
                analyzed_set['parameters'])

        run.measurements = _measurements.Measurement.from_dict(
                analyzed_set['sem'])

        return run

#    @property
#    def parameters_dict(self):
#        return dict((p.name, p.value) for p in self.parameters)
#
#
#    def get_parameter(self, name):
#        return _parameters.SimulationParameter.query.filter_by(run=self,
#                name=name).first().value

    def get_value(self, name):
        return _parameters.SimulationValue.query.filter_by(run=self,
                name=name).first().value

    def get_measurement(self, name):
        return _measurements.Measurement.query.filter_by(run=self,
                name=name).first().as_tuple
