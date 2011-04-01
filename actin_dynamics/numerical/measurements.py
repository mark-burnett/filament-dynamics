#    Copyright (C) 2010-2011 Mark Burnett
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
import bisect
import itertools

import numpy

from actin_dynamics.numerical import workalike


def time_slice(measurement, start_time=None, stop_time=None):
    start_index = 0
    stop_index  = len(measurement[0])
    if start_time is not None:
        start_index = bisect.bisect_left(measurement[0], start_time)
    if stop_time is not None:
        stop_index = bisect.bisect_right(measurement[0], stop_time)

    sliced_measurement = []
    for component in measurement:
        sliced_measurement.append(component[start_index:stop_index])

    return sliced_measurement

def add_number(measurement, number):
    result = [list(component) for component in measurement]

    for i, row in enumerate(zip(*result)):
        old_value = float(result[1][i])
        result[1][i] += number
        if 3 == len(result):
            result[2][i] *= result[1][i] / old_value

    return result


def scale(measurement, factor):
    time = measurement[0]
    rest = measurement[1:]

    scaled_rest = []
    for component in rest:
        scaled_rest.append([c * factor for c in component])

    return list([time]) + scaled_rest


def add(measurements):
    times, values, errors = copy.copy(measurements[0])

    errors = [e**2 for e in errors]

    for mtimes, mvalues, merrors in measurements[1:]:
        merrors = [e**2 for e in merrors]

        values = workalike.add(values, mvalues)
        errors = workalike.add(errors, merrors)

    errors = map(math.sqrt, errors)

    return times, values, errors

def derivative(measurement):
    times, values, errors = measurement
    dv = numpy.diff(values)
    dt = numpy.diff(times)
    return [n/d for n, d in itertools.izip(dv, dt)]
