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

import itertools as _itertools

import elixir as _elixir

from . import mixins as _mixins

class MeasurementValue(_elixir.Entity, _mixins.GetOrCreate):
    _elixir.using_options(tablename='measurement_value',
                          order_by=['measurement_id', 'time'])

    measurement = _elixir.ManyToOne('Measurement')

    time  = _elixir.Field(_elixir.Float())
    value = _elixir.Field(_elixir.Float())
    error = _elixir.Field(_elixir.Float())

    @classmethod
    def from_list(cls, measurement):
        results = [cls(time=t, value=v, error=e)
                   for t, v, e in _itertools.izip(*measurement)]

        return results
