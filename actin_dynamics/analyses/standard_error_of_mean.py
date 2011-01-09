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

import math

import numpy

from . import utils

def all_measurements(input_parameter_sets, output_parameter_sets,
                     error_suffix='_error'):
    for input_ps in input_parameter_sets:
        output_ps = output_parameter_sets.create_or_select_child(input_ps.name)

        summarize_simulation_measurements(input_ps, output_ps, error_suffix)
        summarize_filament_measurements(input_ps, output_ps, error_suffix)


# XXX This function is almost identical to the next.
def summarize_simulation_measurements(input_ps, output_ps, error_suffix=None):
    measurement_names = _get_simulation_measurement_names(input_ps)

    for measurement_name in measurement_names:
        all_values = []
        for simulation in input_ps.simulations:
            measurement = getattr(simulation.simulation_measurements,
                                  measurement_name)
            times, values = zip(*measurement.read())
            all_values.append(values)

        means, errors = analyize_values(all_values)

        utils.write_measurement(output_ps, measurement_name,
                                (times, means, errors),
                                error_suffix=error_suffix)


# XXX This function is almost identical to the previous.
def summarize_filament_measurements(input_ps, output_ps, error_suffix=None):
    measurement_names = _get_filament_measurement_names(input_ps)
    print measurement_names

    for measurement_name in measurement_names:
        all_values = []
        for simulation in input_ps.simulations:
            for filament in simulation.filaments:
                measurement = getattr(filament.measurements,
                                      measurement_name)
                times, values = zip(*measurement.read())
            all_values.append(values)

        means, errors = analyize_values(all_values)

        utils.write_measurement(output_ps, measurement_name,
                                (times, means, errors),
                                error_suffix=error_suffix)


def analyize_values(values):
    '''
    Workhorse function.  Calculates the standard error of the mean.
    '''
    sqrt_N = math.sqrt(len(values))
    transposed_values = numpy.array(values).transpose()

    means  = []
    errors = []
    for tv in transposed_values:
        means.append(numpy.average(tv))
        errors.append(numpy.std(tv) / sqrt_N)

    return means, errors


def _get_filament_measurement_names(parameter_set):
    first_simulation = next(iter(parameter_set.simulations))
    first_filament = next(iter(first_simulation.filaments))
    return [m.name for m in first_filament.measurements]

def _get_simulation_measurement_names(parameter_set):
    first_simulation = next(iter(parameter_set.simulations))
    return [m.name for m in first_simulation.simulation_measurements]
