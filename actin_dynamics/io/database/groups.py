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

class Group(_elixir.Entity, _mixins.Convenience):
    _elixir.using_options(tablename='group')

    name        = _elixir.Field(_elixir.String(50))
    description = _elixir.Field(_elixir.String)

    timestamp = _elixir.Field(_elixir.DateTime)
    revision  = _elixir.Field(_elixir.String(50))

    runs = _elixir.OneToMany('Run')
