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

import pylab as _pylab

from actin_dynamics.io import hdf as _hdf

def plot_length(hdf_file=None, parameter_set_number=None,
                simulation_number=None, standard_deviation=True):
    _pylab.figure()
    results = get_length(hdf_file, parameter_set_number, simulation_number,
                         standard_deviation)
    for r in results:
        print r

    _pylab.plot(*results)
    _pylab.show()

# XXX This function should be refactored into a function that grabs data
# from hdf, and one that actually does the reshaping.
def get_length(hdf_file=None, parameter_set_number=None,
               simulation_number=None, standard_deviation=True):
    parameter_sets, analysis = _hdf.utils.get_ps_ana(hdf_file)

    average_analysis = analysis.average
    average_par_set = average_analysis.select_child_number(parameter_set_number)

    if simulation_number is None:
        # use parameter_set summary data
        length_measurement = average_par_set.measurement_summary.length.read()
    else:
        # get simulation's numbers
        simulation = average_par_set.simulations.select_child_number(
                simulation_number)
        length_measurement = simulation.measurements.length.read()

    # subtract initial filament value
    times, values = zip(*length_measurement)

    # get relavent simulation parameters
    # XXX These should be passed in as parameters.
    parameter_set = parameter_sets.select_child_number(parameter_set_number)
    average_initial_filament_length = parameter_set.parameters[
            'average_initial_filament_length']
    ftc = parameter_set.parameters['filament_tip_concentration']

    # multiply by filament tip concentration
    normalized_values = [(v - average_initial_filament_length) * ftc for v in values]

    if standard_deviation:
        std_analysis = analysis.standard_deviation
        std_par_set = std_analysis.select_child_number(parameter_set_number)

        if simulation_number is None:
            std_measurement = std_par_set.measurement_summary.length.read()

        else:
            std_simulation = std_par_set.simulations.select_child_number(
                    simulation_number)
            std_measurement = std_simulation.measurements.length.read()

        std_times, std_values = zip(*std_measurement)
        normalized_std_values = [s * ftc for s in std_values]

        upper_bound = []
        lower_bound = []
        for nv, ns in zip(normalized_values, normalized_std_values):
            upper_bound.append(nv + ns)
            lower_bound.append(nv - ns)

        return times, normalized_values, times, upper_bound, times, lower_bound
    else:
        return times, normalized_values
