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
import itertools
import math

import numpy

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


def chi_squared(data, sim_avg, sim_std):
    return (sum(((d - a) / s)**2
                for d, a, s in itertools.izip(data, sim_avg, sim_std))
            / len(data))
