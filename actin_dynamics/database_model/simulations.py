#    Copyright (C) 2010 Mark Burnett
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

from .concentrations import Concentration as _Concentration
from .end_conditions import EndCondition as _EndCondition
from .explicit_measurements import ExplicitMeasurement as _ExplicitMeasurement
from .transitions import Transition as _Transition

from .strand_factories import StrandFactory as _StrandFactory

class Simulation(_elixir.Entity):
    _elixir.using_options(tablename='simulation')

    name = _elixir.Field(_elixir.Unicode(50), unique=True)
    description = _elixir.Field(_elixir.UnicodeText)
    creation_date = _elixir.Field(_elixir.DateTime)

    # NOTE This is really one to one ish (because it's a pass-through)
    strand_factory = _elixir.ManyToOne('StrandFactory')

    transitions = _elixir.OneToMany('Transition')
    concentrations = _elixir.OneToMany('Concentration')
    end_conditions = _elixir.OneToMany('EndCondition')
    explicit_measurements = _elixir.OneToMany('ExplicitMeasurement')

    parameter_set_groups = _elixir.OneToMany('ParameterSetGroup')

    @classmethod
    def from_xml(cls, element):
        sf = _StrandFactory.from_xml(element.find('strand_factory'))
        result = cls(name=element.get('name'),
                     description=element.get('description'),
                     strand_factory=sf)

        concentrations = []
        for c in element.find('concentrations'):
            result.concentrations.append(
                    _Concentration.from_xml(c))

        end_conditions = []
        for ec in element.find('end_conditions'):
            result.end_conditions.append(
                    _EndCondition.from_xml(ec))

        explicit_measurements = []
        for em in element.find('expilcit_measurements'):
            result.explicit_measurements.append(
                    _ExplicitMeasurement.from_xml(cm))

        transitions = []
        for t in element.find('transitions'):
            result.transitions.append(
                    _Transition.from_xml(t))

        return result


class SimulationResult(_elixir.Entity):
    _elixir.using_options(tablename='simulation_result')

    parameter_set = _elixir.ManyToOne('ParameterSet')

    timestamp = _elixir.Field(_elixir.DateTime)
    revision = _elixir.Field(_elixir.Integer)

    measurement_data = _elixir.OneToMany('MeasurementData')
