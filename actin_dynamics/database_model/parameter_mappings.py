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

from .parameter_labels import ParameterLabel as _ParameterLabel

class ParameterMapping(_elixir.Entity):
    _elixir.using_options(tablename='parameter_mapping')

    binding = _elixir.ManyToOne('Binding')
    parameter_label = _elixir.ManyToOne('ParameterLabel')
    local_name  = _elixir.Field(_elixir.Unicode(50))

    @classmethod
    def from_xml(cls, element):
        pl = _ParameterLabel.get_by(name=element.get('parameter_label_name'))
        return cls(parameter_label=pl, local_name=element.get('local_name'))
