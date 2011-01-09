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

import pylab

from actin_dynamics import io

from . import basic
from . import utils

from actin_dynamics.analyses import utils as ana_utils

def full_run(hdf_file=None, parameter_set_number=None, parameter_labels=[],
             fluorescence_filename='pollard_length.dat',
             adppi_filename='pollard_cleavage.dat'):
    # Load the data.
    fluor_data = io.data.load_data(fluorescence_filename)
    adppi_data = io.data.load_data(adppi_filename)

    # Plot the data.
    basic.plot_scatter_measurement(adppi_data, color='black')
    basic.plot_smooth_measurement(fluor_data, color='green', linewidth=2)

    # HDF data access.
    simulations, analysis = io.hdf.utils.get_ps_ana(hdf_file)

    parameters = simulations.select_child_number(parameter_set_number).parameters

    pollard_parameter_sets = analysis.create_or_select_child('pollard')
    pollard_ps = pollard_parameter_sets.select_child_number(parameter_set_number)

    average_parameter_sets = analysis.create_or_select_child('average')
    average_ps = average_parameter_sets.select_child_number(parameter_set_number)

    # Get and plot the simulation results.
    # Fluorescence
    fluor_sim = utils.get_measurement_and_error(pollard_ps.measurement_summary,
            'pyrene_fluorescence')
    basic.plot_smooth_measurement(fluor_sim, color='green', fill_alpha=0.3,
                                  linestyle='dashed')

    # F-ADP-Pi-actin
    ftc = parameters['filament_tip_concentration']
    adppi_measurement = ana_utils.get_measurement(average_ps, 'pyrene_adppi_count')

    scaled_adppi = ana_utils.scale_measurement(adppi_measurement, ftc)

    basic.plot_smooth_measurement(scaled_adppi, color='blue', fill_alpha=0.3,
                                  linestyle='dashed')

    # Misc. configuration
    pylab.xlim((0, 45))
    pylab.ylim((0, 7))

    pylab.show()
