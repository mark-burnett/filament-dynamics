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
from . import measurement_values as _measurement_values

class Measurement(_elixir.Entity, _mixins.Convenience):
    _elixir.using_options(tablename='measurement')

    name   = _elixir.Field(_elixir.String(50))

    run    = _elixir.ManyToOne('Run')
    values = _elixir.OneToMany('MeasurementValue')

    @classmethod
    def from_dict(cls, measurements):
        results = []
        for name, measurement in measurements.iteritems():
            m = cls(name=name)
            m.values = _measurement_values.MeasurementValue.from_list(
                    measurement)
            results.append(m)

        return results

    @property
    def as_tuple(self):
        times = []
        values = []
        errors = []
        for mv in self.values:
            times.append(mv.time)
            values.append(mv.value)
            errors.append(mv.error)

        return times, values, errors
