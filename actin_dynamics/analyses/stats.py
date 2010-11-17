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

def average_all(input_parameter_sets, output_parameter_sets):
    return lol_refactor(input_parameter_sets, output_parameter_sets,
                        function=numpy.average)

def std_all(input_parameter_sets, output_parameter_sets):
    return lol_refactor(input_parameter_sets, output_parameter_sets,
                        function=numpy.std)


def lol_refactor(input_parameter_sets, output_parameter_sets, function=None):
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




def get_lengths(filaments_group):
    results = []
    for filament in filaments_group:
        filament_lengths = filament.length.read()
        results.append([fl[0] for fl in filament_lengths])
    return results
