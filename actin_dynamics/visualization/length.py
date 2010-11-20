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

from actin_dynamics.io.hdf.utils import unpack_measurement as _unpack


# XXX This function should be refactored into a function that grabs data
# from hdf, and one that actually does the reshaping.
def get_length(hdf_file=None, parameter_set_number=None,
               simulation_number=None, standard_deviation=True):
    parameter_sets, analysis = _hdf.utils.get_ps_ana(hdf_file)

    average_analysis = analysis.average
    average_par_set = average_analysis.select_child_number(parameter_set_number)

    # get relavent simulation parameters
    # XXX These should probably be passed in as parameters.
    parameter_set = parameter_sets.select_child_number(parameter_set_number)
    average_initial_filament_length = parameter_set.parameters[
            'average_initial_filament_length']
    filament_tip_concentration = parameter_set.parameters[
            'filament_tip_concentration']

    if simulation_number is None:
        # use parameter_set summary data
        times, values = _unpack(average_par_set.measurement_summary.length,
                                shift=-average_initial_filament_length,
                                scaling=filament_tip_concentration)
    else:
        # get simulation's numbers
        simulation = average_par_set.simulations.select_child_number(
                simulation_number)
        times, values = _unpack(simulation.measurements.length,
                                shift=-average_initial_filament_length,
                                scaling=filament_tip_concentration)

    if standard_deviation:
        std_analysis = analysis.standard_deviation
        std_par_set = std_analysis.select_child_number(parameter_set_number)

        if simulation_number is None:
            stimes, stds = _unpack(std_par_set.measurement_summary.length,
                                   scaling=filament_tip_concentration)
        else:
            std_simulation = std_par_set.simulations.select_child_number(
                    simulation_number)
            stimes, stds = _unpack(std_simulation.measurements.length,
                                   scaling=filament_tip_concentration)

        upper_bound = []
        lower_bound = []
        for nv, ns in zip(values, stds):
            upper_bound.append(nv + ns)
            lower_bound.append(nv - ns)

        return times, normalized_values, lower_bound, upper_bound
    else:
        return times, normalized_values
