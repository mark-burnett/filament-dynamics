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

import bisect

import pylab
import numpy

from actin_dynamics import io

from . import basic
from . import parameters
from . import utils

from actin_dynamics.analysis import utils as ana_utils

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


def fit(analysis_container, #weights={'pyrene_fit_naked_chi_squared': 1},
        weights={'adppi_fit_chi_squared': 1},
        pyrene_measurement='pyrene_fit_naked_chi_squared'):
    rates, coops, ftcs, z_values = get_fitnesses(analysis_container, weights)

    best = get_best_par_set(analysis_container, weights=weights)
    parameters = best['parameters']

    pylab.figure()
    title = ('weights = %s\nftc = %s, rate = %s, cooperativity = %s' %
             (weights, parameters['filament_tip_concentration'],
              parameters['cleavage_rate'],
              parameters['cleavage_cooperativity']))
    pylab.suptitle(title)

    pylab.subplot(2, 2, 1)
    basic.plot_contour(rates, coops, z_values,
                       reduction_axis=2,
                       xlabel='Cleavage Rate (s^-1)',
                       ylabel='Cleavage Cooperativity',
                       logscale_y=True,
                       logscale_z=True)

    pylab.subplot(2, 2, 2)
    basic.plot_contour(ftcs, coops, z_values,
                       reduction_axis=0,
                       xlabel='Filament Tip Concentration (uM)',
                       ylabel='Cleavage Cooperativity',
                       logscale_y=True,
                       logscale_z=True,
                       transpose=False)
       
    pylab.subplot(2, 2, 3)
    basic.plot_contour(rates, ftcs, z_values,
                       reduction_axis=1,
                       xlabel='Cleavage Rate (s^-1)',
                       ylabel='Filament Tip Concentration (uM)',
                       logscale_z=True)
       
    pylab.subplot(2, 2, 4)
    plot_full_par_set(best, pyrene_measurement=pyrene_measurement)

    pylab.show()


def get_fitnesses(analysis_container, weights):
    rates = utils.get_parameter_values(analysis_container, 'cleavage_rate')
    coops = utils.get_parameter_values(analysis_container,
                                       'cleavage_cooperativity')
    ftcs = utils.get_parameter_values(analysis_container,
                                      'filament_tip_concentration')

    fitnesses = -numpy.ones((len(rates), len(coops), len(ftcs)))
    for parameter_set in analysis_container:
        parameters = parameter_set['parameters']

        ri = bisect.bisect_left(rates, parameters['cleavage_rate'])
        ci = bisect.bisect_left(coops, parameters['cleavage_cooperativity'])
        fi = bisect.bisect_left(ftcs, parameters['filament_tip_concentration'])

        current_value = _weighted_value(parameter_set['values'], weights)

        if -1 == fitnesses[ri, ci, fi]:
            fitnesses[ri, ci, fi] = current_value
        else:
            fitnesses[ri, ci, fi] = min(current_value, fitnesses[ri, ci, fi])

    return rates, coops, ftcs, fitnesses


def _weighted_value(par_set_values, weights):
    return sum(par_set_values[name] * weight
               for name, weight in weights.iteritems())


def get_best_par_set(analysis_container, weights=None):
    best = None
    for par_set in analysis_container:
        value = _weighted_value(par_set['values'], weights)
        if not best or value < best:
            best = value
            best_par_set = par_set
    return best_par_set


def plot_full_par_set(parameter_set, parameter_labels=[],
           fluorescence_filename='pollard_length.dat',
           adppi_filename='pollard_cleavage.dat',
           pyrene_measurement='pyrene_naked_chi_squared',
           fill_alpha=0.2, trace_alpha=0.1,
           fluorescence_color=FACTIN_FLUORESCENCE_COLOR,
           adppi_color=FACTIN_ADPPI_COLOR,
           factin_color=FACTIN_FACTIN_COLOR):
    # Load the data.
    fluor_data = io.data.load_data(fluorescence_filename)
    adppi_data = io.data.load_data(adppi_filename)

    parameters = parameter_set['parameters']

    # Scale fluorescence data to end at 1
    final_fluorescence_value = fluor_data[1][-1]
    fluor_data = ana_utils.scale_measurement(fluor_data,
                                             2 / final_fluorescence_value)

    # Plot the data.
    basic.plot_scatter_measurement(adppi_data, label='F-ADPPi Data',
                                   color=adppi_color)
    basic.plot_smooth_measurement(fluor_data, label='Pyrene Data',
                                  color=fluorescence_color,
                                  linewidth=2)

    # Used parameters
    ftc = parameters['filament_tip_concentration']
    seed_concentration = parameters['seed_concentration']

    # Get and plot the simulation results.
    # Fluorescence
    fluor_sim = parameter_set['sem'][pyrene_measurement]
    fluor_sim = ana_utils.scale_measurement(fluor_sim,
                                            2 / final_fluorescence_value)
    basic.plot_smooth_measurement(fluor_sim, label='Pyrene Sim',
                                  color=fluorescence_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')

    # F-ADP-Pi-actin
    adppi_measurement = parameter_set['sem']['pyrene_adppi_count']

    scaled_adppi = ana_utils.scale_measurement(adppi_measurement, ftc)

    basic.plot_smooth_measurement(scaled_adppi, label='F-ADPPi Sim',
                                  color=adppi_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')

    # Simulated F-actin concentration
    length_sim = parameter_set['sem']['length']
    scaled_length = ana_utils.scale_measurement(length_sim, ftc)
    subtraced_length = ana_utils.add_number(scaled_length, -seed_concentration)

    basic.plot_smooth_measurement(subtraced_length, label='F-actin Sim',
                                  color=factin_color,
                                  fill_alpha=fill_alpha,
                                  linestyle='dashed')

#    for filament in ana_utils.iter_filaments(parameter_set['downsampled']):
#        # Length
#        length = filament['measurements']['length']
#        scaled_length = ana_utils.scale_measurement(length, ftc)
#        subtraced_length = ana_utils.add_number(scaled_length,
#                                                -seed_concentration)
#        basic.plot_smooth_measurement(subtraced_length,
#                                      color=factin_color,
#                                      line_alpha=trace_alpha)
#
#        # ADPPi
#        adppi_count = filament['measurements']['pyrene_adppi_count']
#        scaled_adppi = ana_utils.scale_measurement(adppi_count, ftc)
#        basic.plot_smooth_measurement(scaled_adppi,
#                                      color=adppi_color,
#                                      line_alpha=trace_alpha)

    # Misc. configuration
    pylab.xlim((0, 41))
    pylab.ylim((0, 7))

    pylab.xlabel('Time (s)')
    pylab.ylabel('Concentration (uM)')

#    pylab.legend(numpoints=1, loc=7)


def goodness_of_fit_1d(analysis_container,
                       ftc=True,
                       cleavage_rate=False,
                       cleavage_cooperativity=False):
    # values_vs_parameter plots
        # parameters:
            # filament_tip_concentration
            # cleavage_rate
            # cleavage_cooperativity
        # value names:
            # fluorescence fit
            # adppi_fit
    if ftc:
        _gof_helper(analysis_container,
                    parameter_name='filament_tip_concentration',
                    value_names=['adppi_fit', 'fluorescence_fit'],
                    plot_labels=['ADP-Pi', 'Fluorescence'],
                    xlabel='Filament Tip Concentration (uM)',
                    ylabel='Goodness of Fit')

    if cleavage_rate:
        _gof_helper(analysis_container,
                    parameter_name='cleavage_rate',
                    value_names=['adppi_fit', 'fluorescence_fit'],
                    plot_labels=['ADP-Pi', 'Fluorescence'],
                    xlabel='Cleavage Rate (s^-1)',
                    ylabel='Goodness of Fit',
                    logscale_x=True)

    if cleavage_cooperativity:
        _gof_helper(analysis_container,
                    parameter_name='cleavage_cooperativity',
                    value_names=['adppi_fit', 'fluorescence_fit'],
                    plot_labels=['ADP-Pi', 'Fluorescence'],
                    xlabel='Cleavage Cooperativity',
                    ylabel='Goodness of Fit',
                    logscale_x=True)
    
    pylab.show()

    # 2d value_vs_2_parameters
        # parameter pairs:
            # cleavage_rate, cleavage_cooperativity

def _gof_helper(analysis_container, parameter_name=None, value_names=None,
                plot_labels=None, xlabel=None, ylabel=None, title=None,
                legend_loc=None, logscale_x=False, logscale_y=False):
    pylab.figure()
    parameters.values_vs_parameter(analysis_container,
            parameter_name=parameter_name,
            value_names=value_names,
            plot_labels=plot_labels)

    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)


    if logscale_x and logscale_y:
        pylab.loglog()
    elif logscale_x:
        pylab.semilogx()
    elif logscale_y:
        pylab.semilogy()

    if title:
        pylab.title(title)

    pylab.legend(loc=legend_loc)
