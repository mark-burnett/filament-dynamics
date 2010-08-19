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

class HydrolysisState(_elixir.Entity):
    _elixir.using_options(tablename='hydrolysis_state')

    name = _elixir.Field(_elixir.Unicode(50))
    description = _elixir.Field(_elixir.UnicodeText)

class HydrolysisStateMapping(_elixir.Entity):
    _elixir.using_options(tablename='hydrolysis_state_mapping')

    binding = _elixir.ManyToOne('Binding')
    local_name = _elixir.Field(_elixir.Unicode(50))
    state = _elixir.ManyToOne('HydrolysisState')
