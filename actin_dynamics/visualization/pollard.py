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

from actin_dynamics.analysis import utils as ana_utils


# Original Colors
#DEFAULT_FACTIN_COLOR = '#A20000'
#DEFAULT_ADPPI_COLOR  = '#659700'
#DEFAULT_FLUORESCENCE_COLOR = '#006161'

# Color Scheme Designer 3
# http://colorschemedesigner.com/#3M62fw0w0w0w0
blue   = ['#123EAB', '#2A4380', '#06246F', '#466FD5', '#6C8AD5']
purple = ['#640CAB', '#582781', '#3F046F', '#9240D5', '#A468D5']
green  = ['#00B945', '#238B49', '#00782D', '#37DC74', '#63DC90']
orange = ['#FFAB00', '#BF9030', '#A66F00', '#FFC040', '#FFD173']

scheme_index = 0

FACTIN_FACTIN_COLOR       = blue[scheme_index]
FACTIN_FLUORESCENCE_COLOR = purple[scheme_index]
FACTIN_ADPPI_COLOR        = green[scheme_index]

FILAMENT_FACTIN_COLOR = FACTIN_FACTIN_COLOR
FILAMENT_ADPPI_COLOR  = FACTIN_ADPPI_COLOR

CONCENTRATIONS_ATP_COLOR   = blue[scheme_index]
CONCENTRATIONS_ADPPI_COLOR = purple[scheme_index]
CONCENTRATIONS_ADP_COLOR   = green[scheme_index]

CONCENTRATIONS_PI_COLOR    = orange[scheme_index]

def factin(hdf_file=None, parameter_set_number=None, parameter_labels=[],
           fluorescence_filename='pollard_length.dat',
           adppi_filename='pollard_cleavage.dat',
           fill_alpha=0.2,
           fluorescence_color=FACTIN_FLUORESCENCE_COLOR,
           adppi_color=FACTIN_ADPPI_COLOR,
           factin_color=FACTIN_FACTIN_COLOR):
    # Load the data.
    fluor_data = io.data.load_data(fluorescence_filename)
    adppi_data = io.data.load_data(adppi_filename)

    # Scale fluorescence data to end at 1
    final_fluorescence_value = fluor_data[1][-1]
    fluor_data = ana_utils.scale_measurement(fluor_data,
                                             1 / final_fluorescence_value)

    # Plot the data.
    pylab.figure()
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

    sem_parameter_sets = analysis.create_or_select_child('sem')
    sem_ps = sem_parameter_sets.select_child_number(parameter_set_number)

    # Used parameters
    ftc = parameters['filament_tip_concentration']
    seed_concentration = parameters['seed_concentration']

    # Get and plot the simulation results.
    # Fluorescence
    fluor_sim = ana_utils.get_measurement(pollard_ps, 'pyrene_fluorescence')
    fluor_sim = ana_utils.scale_measurement(fluor_sim,
                                            1 / final_fluorescence_value)
    basic.plot_smooth_measurement(fluor_sim, label='Pyrene Sim',
                                  color=fluorescence_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')

    # F-ADP-Pi-actin
    adppi_measurement = ana_utils.get_measurement(sem_ps, 'pyrene_adppi_count')

    scaled_adppi = ana_utils.scale_measurement(adppi_measurement, ftc)

    basic.plot_smooth_measurement(scaled_adppi, label='F-ADPPi Sim',
                                  color=adppi_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')

    # Simulated F-actin concentration
    length_sim = ana_utils.get_measurement(sem_ps, 'length')
    scaled_length = ana_utils.scale_measurement(length_sim, ftc)
    subtraced_length = ana_utils.add_number(scaled_length, -seed_concentration)

    basic.plot_smooth_measurement(subtraced_length, label='F-actin Sim',
                                  color=factin_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')

    # Misc. configuration
    title = utils.parameter_title(parameter_set_number, parameters,
                                   parameter_labels)
    pylab.title(title)

    pylab.xlim((0, 41))
    pylab.ylim((0, 7))

    pylab.xlabel('Time (s)')
    pylab.ylabel('Concentration (uM)')

    pylab.legend(numpoints=1, loc=7)

    pylab.show()


def filaments(hdf_file=None, parameter_set_number=None, parameter_labels=[],
              adppi_filename='pollard_cleavage.dat',
              factin_color=FILAMENT_FACTIN_COLOR,
              adppi_color=FILAMENT_ADPPI_COLOR,
              trace_alpha=0.1,
              fill_alpha=0.2):
    # ADP-Pi data access
    adppi_data = io.data.load_data(adppi_filename)

    # HDF data access.
    simulations, analysis = io.hdf.utils.get_ps_ana(hdf_file)

    parameters = simulations.select_child_number(parameter_set_number).parameters

    downsampled_parameter_sets = analysis.create_or_select_child('downsample')
    parameter_set = downsampled_parameter_sets.select_child_number(
            parameter_set_number)

    sem_parameter_sets = analysis.create_or_select_child('sem')
    sem_ps = sem_parameter_sets.select_child_number(parameter_set_number)

    # Used parameters
    ftc = parameters['filament_tip_concentration']
    seed_concentration = parameters['seed_concentration']

    pylab.figure()
    adppi_data_line = basic.plot_scatter_measurement(adppi_data,
            label='F-ADPPi Data', color=adppi_color)

    for filament in parameter_set.iter_filaments():
        # Length
        length = zip(*filament.measurements.length.read())
        scaled_length = ana_utils.scale_measurement(length, ftc)
        subtraced_length = ana_utils.add_number(scaled_length,
                                                -seed_concentration)
        basic.plot_smooth_measurement(subtraced_length,
                                      color=factin_color,
                                      line_alpha=trace_alpha)

        # ADPPi
        adppi_count = zip(*filament.measurements.pyrene_adppi_count)
        scaled_adppi = ana_utils.scale_measurement(adppi_count, ftc)
        basic.plot_smooth_measurement(scaled_adppi,
                                      color=adppi_color,
                                      line_alpha=trace_alpha)

    length_sim = ana_utils.get_measurement(sem_ps, 'length')
    scaled_length = ana_utils.scale_measurement(length_sim, ftc)
    subtraced_length = ana_utils.add_number(scaled_length, -seed_concentration)

    factin_line = basic.plot_smooth_measurement(subtraced_length,
                                                color=factin_color,
                                                fill_alpha=fill_alpha)

    adppi = ana_utils.get_measurement(sem_ps, 'pyrene_adppi_count')
    scaled_adppi = ana_utils.scale_measurement(adppi, ftc)
    adppi_line = basic.plot_smooth_measurement(scaled_adppi,
                                               color=adppi_color,
                                               fill_alpha=fill_alpha)

    title = utils.parameter_title(parameter_set_number, parameters, parameter_labels)
    pylab.title(title)

    pylab.xlim((0, 41))
    pylab.ylim((0, 7))

    pylab.xlabel('Time (s)')
    pylab.ylabel('Concentration (uM)')

    pylab.legend((adppi_data_line[0], adppi_line, factin_line),
                 ('F-ADP-Pi Data', 'F-ADP-Pi Sim', 'F-actin Sim'),
                 loc=4, numpoints=1)

    pylab.show()


def concentrations(hdf_file=None, parameter_set_number=None, parameter_labels=[],
                   atp_color=CONCENTRATIONS_ATP_COLOR,
                   adppi_color=CONCENTRATIONS_ADPPI_COLOR,
                   adp_color=CONCENTRATIONS_ADP_COLOR,
                   pi_color=CONCENTRATIONS_PI_COLOR,
                   fill_alpha=0.2):
    # HDF setup
    simulations, analysis = io.hdf.utils.get_ps_ana(hdf_file)
    parameters = simulations.select_child_number(parameter_set_number).parameters

    sem_parameter_sets = analysis.create_or_select_child('sem')
    sem_ps = sem_parameter_sets.select_child_number(parameter_set_number)

    # Extract data
    atp_sim = ana_utils.get_measurement(sem_ps, 'pyrene_ATP')
    adppi_sim = ana_utils.get_measurement(sem_ps, 'pyrene_ADPPi')

    pyrene_adp_sim = ana_utils.get_measurement(sem_ps, 'pyrene_ADP')
    adp_sim = ana_utils.get_measurement(sem_ps, 'ADP')
    full_adp_sim = ana_utils.add_measurements(pyrene_adp_sim, adp_sim)

    pi_sim = ana_utils.get_measurement(sem_ps, 'Pi')

    # Actual Plotting
    pylab.figure()
    basic.plot_smooth_measurement(atp_sim, label='ATP-actin',
                                  color=atp_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')
    basic.plot_smooth_measurement(adppi_sim, label='ADP-Pi-actin',
                                  color=adppi_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')
    basic.plot_smooth_measurement(full_adp_sim, label='ADP-actin',
                                  color=adp_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')
    basic.plot_smooth_measurement(pi_sim, label='Pi',
                                  color=pi_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')

    # Misc. configuration
    title = utils.parameter_title(parameter_set_number, parameters,
                                   parameter_labels)
    pylab.title(title)

    pylab.xlim((0, 41))
    pylab.ylim((0, 7))

    pylab.xlabel('Time (s)')
    pylab.ylabel('Concentration (uM)')

    pylab.legend(numpoints=1, loc=7)

    pylab.show()
