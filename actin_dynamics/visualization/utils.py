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

from actin_dynamics.io import hdf as _hdf

def get_measurement_summary(analyses=None, parameter_set_number=None,
                            measurement_name=None):
    average_parameter_set = analyses.average.select_child_number(
            parameter_set_number)
    std_parameter_set = analyses.standard_deviation.select_child_number(
            parameter_set_number)

    times, averages = _unpack_measurement(average_parameter_set,
                                          measurement_name)
    stimes, stds = _unpack_measurement(std_parameter_set, measurement_name)

    upper_bound = []
    lower_bound = []
    for t, ts, a, s in zip(times, stimes, averages, stds):
        assert(t == ts)
        upper_bound.append(a + s)
        lower_bound.append(a - s)

    return times, averages, lower_bound, upper_bound

def _unpack_measurement(parameter_set=None, measurement_name=None):
    measurement = getattr(parameter_set.measurement_summary, measurement_name)
    times  = []
    values = []
    for t, v in measurement.read():
        times.append(t)
        values.append(v)
    return times, values

def scale_measurement(measurement, factor):
    time, average, lower, upper = measurement

    new_average = [a * factor for a in average]
    new_lower   = [l * factor for l in lower]
    new_upper   = [g * factor for g in upper]

    return time, new_average, new_lower, new_upper
