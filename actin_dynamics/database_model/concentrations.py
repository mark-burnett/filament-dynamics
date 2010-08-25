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

from .bindings import Binding as _Binding
from .hydrolysis_states import HydrolysisState as _HydrolysisState
from .measurements import MeasurementLabel as _MeasurementLabel

class Concentration(_elixir.Entity):
    _elixir.using_options(tablename='concentration')

    simulation = _elixir.ManyToOne('Simulation')
    state = _elixir.ManyToOne('HydrolysisState')
    binding = _elixir.ManyToOne('Binding', column_kwargs=dict(unique=True))
    measurement_label = _elixir.ManyToOne('MeasurementLabel')

    @classmethod
    def from_xml(cls, element):
        hs = _HydrolysisState.get_by(name=element.get('state_name'))
        ml = _MeasurementLabel.get_by(
                name=element.get('measurement_label_name'))
        b = _Binding.from_xml(element.find('binding'))
        return cls(state=hs, measurement_label=ml, binding=b)
