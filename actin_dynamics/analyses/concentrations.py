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

from . import interpolation
from . import fitting
from . import utils

def adppi_fit(simulations=None, input_parameter_sets=None,
              output_parameter_sets=None, data=None):
    sample_times, data_values, data_lower_boud, data_upper_bound = data

    for ps_index in xrange(len(input_parameter_sets)):
        input_ps = input_parameter_sets.select_child_number(ps_index)
        parameter_ps = simulations.select_child_number(ps_index)
        ftc = parameter_ps.parameters['filament_tip_concentration']
        # Get and resample simulation results
        # XXX We are only using pyrene adppi, we should be using both.
        raw_sim_data = utils.get_measurement(input_ps, 'pyrene_adppi_count')

        sampled_sim_data = interpolation.resample_measurement(
                raw_sim_data, sample_times)
        scaled_sim_data = utils.scale_measurement(sampled_sim_data, ftc)

        chi_squared = fitting.measurement_chi_squared(scaled_sim_data, data)

        output_ps = output_parameter_sets.create_or_select_child(input_ps.name)
        output_ps.values['adppi_chi_squared'] = chi_squared
