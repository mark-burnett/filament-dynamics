#    Copyright (C) 2011 Mark Burnett
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

from . import basic

from actin_dynamics import io

from actin_dynamics.analysis import accessors
from actin_dynamics.analysis import utils


# Color Scheme Designer 3
# http://colorschemedesigner.com/#3M62fw0w0w0w0
blue   = ['#123EAB', '#2A4380', '#06246F', '#466FD5', '#6C8AD5']
purple = ['#640CAB', '#582781', '#3F046F', '#9240D5', '#A468D5']
green  = ['#00B945', '#238B49', '#00782D', '#37DC74', '#63DC90']
orange = ['#FFAB00', '#BF9030', '#A66F00', '#FFC040', '#FFD173']

LENGTH_COLORS = blue
CLEAVAGE_COLORS = orange
ADPPI_COLORS = green


def plot_full_data(parameter_set):
    # Get data from files.
    pyrene_data, adppi_data = io.pollard.get_data()


    # Get simulation results.
    length_sim = accessors.get_length(parameter_set)
    adppi_sim  = accessors.get_scaled(parameter_set, 'pyrene_adppi_count')
    pyrene_sim = accessors.get_fluorescence(parameter_set)


    # Plot.
    pylab.figure()
    basic.plot_smooth_measurement(pyrene_data, label='Pyrene Data',
                                  color=purple[0])
    basic.plot_smooth_measurement(pyrene_sim, label='Pyrene Sim',
                                  color=purple[1])

    basic.plot_smooth_measurement(length_sim, label='Length Sim',
                                  color=blue[1])

    basic.plot_scatter_measurement(adppi_data, label='F-ADP-Pi Data',
                                   color=green[0])
    basic.plot_smooth_measurement(adppi_sim, label='F-ADP-Pi Sim',
                                  color=green[1])

    pylab.xlim((0, 40))
    pylab.ylim((0, 7))
    pylab.legend(loc=4)


def kinsim_compare(parameter_set):
    pollard_length_sim, pollard_cleavage_sim = io.pollard.get_simulations()
    kin_factin_sim, kin_pi_sim, kin_atp_sim = io.pollard.get_kinsim()

    # Useful parameters
    ftc = parameter_set['parameters']['filament_tip_concentration']
    seed_conc = parameter_set['parameters']['seed_concentration']

    # Get simulation results.
    length_sim   = accessors.get_length(parameter_set)
    cleavage_sim = accessors.get_scaled(parameter_set, 'cleavage')
    adppi_sim    = accessors.get_scaled(parameter_set, 'pyrene_adppi_count')
    atp_sim      = accessors.get_scaled(parameter_set, 'pyrene_atp_count')

    # Start doing some real plotting!
    pylab.figure()
    basic.plot_smooth_measurement(kin_factin_sim, label='KINSIM F-actin',
                                  color=blue[0])
    basic.plot_smooth_measurement(pollard_length_sim,
                                  label='Pollard F-actin',
                                  color=blue[1])
    basic.plot_smooth_measurement(length_sim, label='My F-actin',
                                  color=blue[2])

    basic.plot_smooth_measurement(adppi_sim, label='My F-ADP-Pi',
                                  color=green[1])

    basic.plot_smooth_measurement(kin_pi_sim, label='KINSIM Cleavage',
                                  color=orange[0])
    basic.plot_smooth_measurement(cleavage_sim, label='My Cleavage',
                                  color=orange[1])
    basic.plot_smooth_measurement(pollard_cleavage_sim,
                                  label='Pollard Cleavage',
                                  color=orange[2])

    basic.plot_smooth_measurement(kin_atp_sim, label='KINSIM F-ATP',
                                  color=purple[1])
    basic.plot_smooth_measurement(atp_sim, label='My F-ATP',
                                  color=purple[1])

    pylab.xlim((0, 40))
    pylab.ylim((0, 7))
    pylab.legend(loc=5)
