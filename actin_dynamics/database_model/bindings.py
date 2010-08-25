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

from .parameter_mappings import ParameterMapping as _ParameterMapping
from .hydrolysis_states import HydrolysisStateMapping as _HydrolysisStateMapping 

class Binding(_elixir.Entity):
    _elixir.using_options(tablename='binding')

    class_name = _elixir.Field(_elixir.Unicode(50))
    parameter_mappings = _elixir.OneToMany('ParameterMapping')
    state_mappings = _elixir.OneToMany('HydrolysisStateMapping')

    @classmethod
    def from_xml(cls, element):
        parameter_mappings = []
        for pm_xml in element.find('parameter_mappings'):
            parameter_mappings.append(_ParameterMapping.from_xml(pm_xml))

        state_mappings = []
        for sm_xml in element.find('state_mappings'):
            state_mappings.append(_HydrolysisStateMapping.from_xml(sm_xml))

        return cls(class_name=element.get('class_name'),
                   parameter_mappings=parameter_mappings,
                   state_mappings=state_mappings)
