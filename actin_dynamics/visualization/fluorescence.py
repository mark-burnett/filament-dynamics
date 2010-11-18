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

def get_flourescence(hdf_file=None, parameter_set_number=None,
                     simulation_number=None, coefficients=None,
                     normalization=1, standard_deviation=True):
    parameter_sets, analysis = _hdf.utils.get_ps_ana(hdf_file)

    average_analysis = analysis.average
    average_par_set = average_analysis.select_child_number(parameter_set_number)

    if simulation_number is None:
        # use parameter_set summary data
        atp_count   = average_par_set.measurement_summary.atp_count.read()
        adppi_count = average_par_set.measurement_summary.adppi_count.read()
        adp_count   = average_par_set.measurement_summary.adp_count.read()
    else:
        # get simulation's numbers
        simulation = average_par_set.simulations.select_child_number(
                simulation_number)
        raw_atp_count   = simulation.measurements.atp_count.read()
        raw_adppi_count = simulation.measurements.adppi_count.read()
        raw_adp_count   = simulation.measurements.adp_count.read()

    times, atp_count   = zip(*raw_atp_count)
    times, adppi_count = zip(*raw_adppi_count)
    times, adp_count   = zip(*raw_adp_count)

    parameter_set = parameter_sets.select_child_number(parameter_set_number)
    ftc = parameter_set.parameters['filament_tip_concentration']

    normalized_atp   = [(v - atp_count[0]) * ftc / normalization
                        for v in atp_count]
    normalized_adppi = [(v - adppi_count[0]) * ftc / normalization
                        for v in adppi_count]
    normalized_adp   = [(v - adp_count[0]) * ftc / normalization
                        for v in adp_count]

    fluorescence = [t * coefficients['ATP']
                        + p * coefficients['ADPPi']
                        + d * coefficients['ADP']
                    for t, p, d in zip(normalized_atp, normalized_adppi,
                                       normalized_adp)]
    return times, fluorescence
