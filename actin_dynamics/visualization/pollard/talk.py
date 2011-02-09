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

import itertools

import numpy
import pylab

from .. import slicing
from .. import measurements

from . import fit_1d

COLORS = numpy.array([
        ['#06246F', '#2A4380', '#123EAB', '#466FD5', '#6C8AD5'],  # blue
        ['#3F046F', '#582781', '#640CAB', '#9240D5', '#A468D5'],  # purple
        ['#00782D', '#238B49', '#00B945', '#37DC74', '#63DC90'],  # green
        ['#A66F00', '#BF9030', '#FFAB00', '#FFC040', '#FFD173']]) # orange

def random_adppi(group):
    slicer = slicing.Slicer.from_group(group, 'pollard_adppi_chi_squared',
                                run_parameters=['filament_tip_concentration',
                                                'cleavage_rate'],
                                table_name='rra')

    pylab.figure()

    pylab.subplot(1,2,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0,14)

    pylab.subplot(1,2,2)
    fit_1d.simple(slicer, 'cleavage_rate',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0,14)

    pylab.figure()

    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'filament_tip_concentration'])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()

def random_length(group):
    slicer = slicing.Slicer.from_group(group, 'pollard_length_chi_squared',
                                run_parameters=['filament_tip_concentration',
                                                'cleavage_rate'],
                                table_name='rrf')

    pylab.figure()

    pylab.subplot(1,2,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('F-actin Fit (AU)')
    pylab.ylim(0,0.6)

    pylab.subplot(1,2,2)
    fit_1d.simple(slicer, 'cleavage_rate',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('F-actin Fit (AU)')
    pylab.ylim(0,0.6)

    pylab.figure()

    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'filament_tip_concentration'])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()

def coop_adppi(group):
    slicer = slicing.Slicer.from_group(group, 'pollard_adppi_chi_squared',
                                run_parameters=['filament_tip_concentration',
                                                'cleavage_rate',
                                                'cleavage_cooperativity'],
                                table_name='cra')

    pylab.figure()

    pylab.subplot(1,3,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, 14)

    pylab.subplot(1,3,2)
    fit_1d.simple(slicer, 'cleavage_rate',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, 14)

    pylab.subplot(1,3,3)
    fit_1d.simple(slicer, 'cleavage_cooperativity',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3],
                  logscale_x=True)
    pylab.xlabel('Cleavage Cooperativity')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, 14)

    pylab.figure()

    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'filament_tip_concentration'])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()

def coop_length(group):
    slicer = slicing.Slicer.from_group(group, 'pollard_length_chi_squared',
                                run_parameters=['filament_tip_concentration',
                                                'cleavage_rate',
                                                'cleavage_cooperativity'],
                                table_name='crl')

    pylab.figure()

    pylab.subplot(1,3,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, 0.6)

    pylab.subplot(1,3,2)
    fit_1d.simple(slicer, 'cleavage_rate',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, 0.6)

    pylab.subplot(1,3,3)
    fit_1d.simple(slicer, 'cleavage_cooperativity',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3],
                  logscale_x=True)
    pylab.xlabel('Cleavage Cooperativity')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, 0.6)

    pylab.figure()

    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'filament_tip_concentration'])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()
