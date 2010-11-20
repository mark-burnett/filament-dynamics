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

def all_parameter_sets(hdf_file=None, coefficients=None, normalization=1):
    parameter_sets, all_analyses = _hdf.utils.get_ps_ana(hdf_file)

    fl_analysis = all_analyses.create_or_select_child(name='fluorescence')

    for ps in parameter_sets:
        ps_results = fl_analysis.create_or_select_child(name=ps.name)
        single_parameter_set(ps, ps_results, coefficients=coefficients,
                             normalization=normalization)

def single_parameter_set(parameter_set, analysis_set):
    pass


def get_flourescence(hdf_file=None, parameter_set_number=None,
                     simulation_number=None, coefficients=None,
                     normalization=1):
    parameter_sets, analysis = _hdf.utils.get_ps_ana(hdf_file)

    if coefficients is None:
        # XXX These may not match literature values, I can't check now.
        coefficients = {'ATP': 0.35,
                        'ADPPi': 0.56,
                        'ADP': 0.75}

    average_analysis = analysis.average
    average_par_set = average_analysis.select_child_number(parameter_set_number)

    # Parameters
    parameter_set = parameter_sets.select_child_number(parameter_set_number)
    filament_tip_concentration = parameter_set.parameters[
            'filament_tip_concentration']

    scaling = filament_tip_concentration / normalization

    if simulation_number is None:
        # use parameter_set summary data
        times, atp_count = _unpack(average_par_set.measurement_summary.atp_count,
                                   scaling=scaling)
        jtimes, adppi_count = _unpack(
                average_par_set.measurement_summary.adppi_count,
                scaling=scaling)
        jtimes, adp_count = _unpack(
                average_par_set.measurement_summary.adp_count,
                scaling=scaling)
    else:
        # get simulation's numbers
        simulation = average_par_set.simulations.select_child_number(
                simulation_number)
        times, atp_count = _unpack(simulation.measurements.atp_count,
                                   scaling=scaling)
        jtimes, adppi_count = _unpack(simulation.measurements.adppi_count,
                                      scaling=scaling)
        jtimes, adp_count = _unpack(simulation.measurements.adp_count,
                                    scaling=scaling)

    fluorescence = [t * coefficients['ATP']
                        + p * coefficients['ADPPi']
                        + d * coefficients['ADP']
                    for t, p, d in zip(normalized_atp, normalized_adppi,
                                       normalized_adp)]
    return times, fluorescence
