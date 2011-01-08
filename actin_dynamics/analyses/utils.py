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

import copy
import math

import numpy

from actin_dynamics.io import hdf as _hdf

# XXX Delete this
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

# XXX Delete this
def _unpack_measurement(parameter_set=None, measurement_name=None):
    measurement = getattr(parameter_set.measurement_summary, measurement_name)
    times  = []
    values = []
    for t, v in measurement.read():
        times.append(t)
        values.append(v)
    return times, values


def get_measurement(parameter_set, measurement_name, error_type='filament'):
    '''
    Gets a measurement calculates its standard error.
    '''
    times, values = zip(*getattr(parameter_set.measurement_summary,
                                 measurement_name).read())

    if 'filament' == error_type:
        N = parameter_set.values['num_filaments']
    elif 'simulation' == error_type:
        N = parameter_set.values['num_simulations']

    scale = 1.0 / math.sqrt(float(N))
    errors = [v * scale for v in values]

    return times, values, errors

def scale_measurement(measurement, factor):
    time = measurement[0]
    rest = measurement[1:]

    scaled_rest = []
    for component in rest:
        scaled_rest.append([c * factor for c in component])

    return list([time]) + scaled_rest

def add_measurements(errors=True, *measurements):
    if errors:
        times, values, errors = copy.copy(measurements[0])

        values = numpy.array(values)
        errors = numpy.power(errors, 2)

        for mtimes, mvalues, merrors in measurements[1:]:
            mvalues = numpy.array(mvalues)
            merrors = numpy.power(merrors, 2)

            values += mvalues
            errors += merrors

        errors = numpy.sqrt(errors)

        return times, values, errors
    else:
        raise NotImplementedError()
