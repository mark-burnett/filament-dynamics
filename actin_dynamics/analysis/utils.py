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

import numpy

def write_measurement(parameter_set, measurement_name,
                      measurement, error_suffix='_error'):
    output = parameter_set.measurement_summary.create_or_select_child(
            measurement_name)
    output.write(zip(*measurement[:2]))
    error = parameter_set.measurement_summary.create_or_select_child(
            measurement_name + error_suffix)
    error.write(zip(measurement[0], measurement[2]))


def get_measurement(parameter_set, measurement_name, error_suffix='_error'):
    '''
    Gets a measurement calculates its standard error.
    '''
    times, values = zip(*getattr(parameter_set.measurement_summary,
                                 measurement_name).read())
    jimes, errors = zip(*getattr(parameter_set.measurement_summary,
                                 measurement_name + error_suffix).read())

    return times, values, errors


def add_number(measurement, number):
    result = [list(component) for component in measurement]

    for i, row in enumerate(zip(*result)):
        old_value = result[1][i]
        result[1][i] += number
        if 3 == len(result):
            result[2][i] *= result[1][i] / old_value

    return result


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
