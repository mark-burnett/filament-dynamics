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

import numpy


def _avg_summary_function(values):
    return [numpy.average(row) for row in values]

def _std_summary_function(values):
    return numpy.sqrt([sum(numpy.power(row, 2)) / len(row)
                       for row in values])

def average_all(input_parameter_sets, output_parameter_sets):
    output_ps = statistics_loop(input_parameter_sets, output_parameter_sets,
                                function=numpy.average)
    summarize_values(output_ps, function=_avg_summary_function)


def std_all(input_parameter_sets, output_parameter_sets):
    output_ps = statistics_loop(input_parameter_sets, output_parameter_sets,
                                function=numpy.std)
    summarize_values(output_ps, function=_std_summary_function)


def statistics_loop(input_parameter_sets, output_parameter_sets, function=None):
    for input_ps in input_parameter_sets:
        output_ps = output_parameter_sets.create_child(input_ps.name)
        for simulation in input_ps.simulations:
            output_sim = output_ps.simulations.create_child(simulation.name)
            for measurement_name in simulation.filament_measurement_names:
                m_stat_results = get_statistics(simulation, measurement_name,
                                                function=function)
                output_measurement = output_sim.measurements.create_child(
                        measurement_name)
                output_measurement.write(m_stat_results)
    return output_parameter_sets

def summarize_values(parameter_sets, function=None):
    for parameter_set in parameter_sets:
        measurement_names = get_parameter_set_measurement_names(parameter_set)
        for measurement_name in measurement_names:
            all_values = []
            for simulation in parameter_set.simulations:
                measurement = getattr(simulation.measurements, measurement_name)
                times, values = zip(*measurement.read())
                all_values.append(values)
            all_values = numpy.array(all_values).transpose()

            summarized_values = function(all_values)

            output_measurement = (
                    parameter_set.measurement_summary.create_or_select_child(
                        measurement_name))
            output_measurement.write(zip(times, summarized_values))


def get_statistics(simulation_wrapper=None, measurement_name=None,
                   function=None):
    all_filaments = []
    for filament in simulation_wrapper.filaments:
        times, values = zip(*getattr(filament.measurements, measurement_name))
        all_filaments.append(values)

    results = []
    for t, vals in zip(times, numpy.array(all_filaments).transpose()):
        results.append((t, function(vals)))
    return results

def get_parameter_set_measurement_names(parameter_set):
    first_simulation = next(iter(parameter_set.simulations))
    return [m.name for m in first_simulation.measurements]
