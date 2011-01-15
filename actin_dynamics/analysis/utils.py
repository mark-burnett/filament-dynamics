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


def iter_filaments(simulations):
    for simulation in simulations:
        for filament in simulation['filaments']:
            yield filament


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

def add_measurements(use_errors=True, *measurements):
    if use_errors:
        times, values, errors = copy.copy(measurements[0])

        errors = [e**2 for e in errors]

        for mtimes, mvalues, merrors in measurements[1:]:
            merrors = [e**2 for e in merrors]

            values = _vectorize_add(values, mvalues)
            errors = _vectorize_add(errors, merrors)

        errors = map(math.sqrt, errors)

        return times, values, errors
    else:
        raise NotImplementedError()
