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

class FloatDict(_elixir.Entity, _mixins.GetOrCreate):
    _elixir.using_options(inheritance='multi', tablename='float_dict')

    name  = _elixir.Field(_elixir.String(64), index=True)
    value = _elixir.Field(_elixir.Float, index=True)

    @classmethod
    def from_dict(cls, parameters):
        results = []
        for name, value in parameters.iteritems():
            results.append(cls(name=name, value=value))

        return results
