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

# Original Colors
# 006161, 659700, A200

# More Colors
# Blue,   Orange, Red
# 005164, A27100, A21300

def full_run(hdf_file=None, parameter_set_number=None, parameter_labels=[],
             fluorescence_filename='pollard_length.dat',
             adppi_filename='pollard_cleavage.dat',
             alpha=0.2,
             fluorescence_color='#006161',
             adppi_color='#659700',
             factin_color='#A20000'):
    # Load the data.
    fluor_data = io.data.load_data(fluorescence_filename)
    adppi_data = io.data.load_data(adppi_filename)

    # Scale fluorescence data to end at 1
    final_fluorescence_value = fluor_data[1][-1]
    fluor_data = ana_utils.scale_measurement(fluor_data,
                                             1 / final_fluorescence_value)

    # Plot the data.
    basic.plot_scatter_measurement(adppi_data, label='F-ADPPi Data',
                                   color=adppi_color)
    basic.plot_smooth_measurement(fluor_data, label='Pyrene Data',
                                  color=fluorescence_color,
                                  linewidth=2)

    # HDF data access.
    simulations, analysis = io.hdf.utils.get_ps_ana(hdf_file)

    parameters = simulations.select_child_number(parameter_set_number).parameters

    pollard_parameter_sets = analysis.create_or_select_child('pollard')
    pollard_ps = pollard_parameter_sets.select_child_number(parameter_set_number)

    average_parameter_sets = analysis.create_or_select_child('sem')
    average_ps = average_parameter_sets.select_child_number(parameter_set_number)

    # Used parameters
    ftc = parameters['filament_tip_concentration']
    seed_concentration = parameters['seed_concentration']

    # Get and plot the simulation results.
    # Fluorescence
    fluor_sim = utils.get_measurement_and_error(pollard_ps.measurement_summary,
            'pyrene_fluorescence')
    fluor_sim = ana_utils.scale_measurement(fluor_sim,
                                            1 / final_fluorescence_value)
    basic.plot_smooth_measurement(fluor_sim, label='Pyrene Sim',
                                  color=fluorescence_color,
                                  fill_alpha=alpha,
                                  linestyle='dashed')

    # F-ADP-Pi-actin
    adppi_measurement = ana_utils.get_measurement(average_ps, 'pyrene_adppi_count')

    scaled_adppi = ana_utils.scale_measurement(adppi_measurement, ftc)

    basic.plot_smooth_measurement(scaled_adppi, label='F-ADPPi Sim',
                                  color=adppi_color,
                                  fill_alpha=alpha,
                                  linestyle='dashed')

    # Simulated F-actin concentration
    length_sim = ana_utils.get_measurement(average_ps, 'length')
    scaled_length = ana_utils.scale_measurement(length_sim, ftc)
    subtraced_length = ana_utils.add_number(scaled_length, -seed_concentration)

    basic.plot_smooth_measurement(subtraced_length, label='F-actin Sim',
                                  color=factin_color,
                                  fill_alpha=alpha,
                                  linestyle='dashed')

    # Display requested parameters
    title = ''
    for label in parameter_labels:
        if title and title[-1] != ' ':
            title += ' -- '
        title += label + ': ' + str(parameters[label])

    # Misc. configuration
    pylab.xlim((0, 41))
    pylab.ylim((0, 7))
    pylab.title(title)

    pylab.xlabel('Time (s)')
    pylab.ylabel('Concentration (uM)')

    pylab.legend(numpoints=1, loc=7)

    pylab.show()
