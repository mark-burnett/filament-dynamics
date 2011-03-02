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

from . import fit_1d

COLORS = numpy.array([
        ['#06246F', '#2A4380', '#123EAB', '#466FD5', '#6C8AD5'],  # blue
        ['#3F046F', '#582781', '#640CAB', '#9240D5', '#A468D5'],  # purple
        ['#00782D', '#238B49', '#00B945', '#37DC74', '#63DC90'],  # green
        ['#A66F00', '#BF9030', '#FFAB00', '#FFC040', '#FFD173']]) # orange

def random_adppi(adppi_ob, pyrene_ob):
    adppi_slicer  = slicing.Slicer.from_objective_bind(adppi_ob)
    pyrene_slicer = slicing.Slicer.from_objective_bind(pyrene_ob)
    max_val = 14
    pylab.figure()

    blvd, best_pyrene_id = pyrene_slicer.get_best_parameters()
#    print 'pyrene best pars', blvd

    fit_1d.simple(adppi_slicer, 'cleavage_rate',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3],
                  filament_tip_concentration=blvd['filament_tip_concentration'])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
#    pylab.ylim(0, max_val)


def random_length(group):
    slicer = slicing.Slicer.from_group(group, 'pollard_length_chi_squared',
                                run_parameters=['filament_tip_concentration',
                                                'cleavage_rate'],
                                table_name='rrf')

    max_val = 0.6

    pylab.figure()

#    pylab.subplot(1,2,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('F-actin Fit (AU)')
    pylab.ylim(0, max_val)

#    pylab.subplot(1,2,2)
#    fit_1d.simple(slicer, 'cleavage_rate',
#                  min_color=COLORS[0][0], slice_color=COLORS[0][3])
#    pylab.xlabel('Cleavage Rate (s^-1)')
#    pylab.ylabel('F-actin Fit (AU)')
#    pylab.ylim(0, max_val)

    pylab.figure()

    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'filament_tip_concentration'],
                   max_val=max_val)
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()


def random_pyrene(pyrene_ob):
    slicer = slicing.Slicer.from_objective_bind(pyrene_ob)
    max_val = 2.5

    pylab.figure()

    pylab.subplot(1,2,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[1][0], slice_color=COLORS[1][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('Pyrene Fit (AU)')
    pylab.ylim(0, max_val)

#    pylab.subplot(1,3,2)
#    fit_1d.simple(slicer, 'cleavage_rate',
#                  min_color=COLORS[1][0], slice_color=COLORS[1][3])
#    pylab.xlabel('Cleavage Rate (s^-1)')
#    pylab.ylabel('Pyrene Fit (AU)')
#    pylab.ylim(0, max_val)

    pylab.subplot(1,2,2)
    fit_1d.simple(slicer, 'pyrene_atp_weight',
                  min_color=COLORS[1][0], slice_color=COLORS[1][3])
    pylab.xlabel('ATP Fluorescence Weight (AU)')
    pylab.ylabel('Pyrene Fit (AU)')
    pylab.ylim(0, max_val)

#    pylab.figure()
#
#    pylab.subplot(1,2,1)
#    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
#                                            'filament_tip_concentration'],
#                   max_val=max_val)
#    pylab.xlabel('Cleavage Rate (s^-1)')
#    pylab.ylabel('Filament Tip Concentration (uM)')
#    pylab.colorbar()
#
#    pylab.subplot(1,2,2)
#    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
#                                            'atp_weight'],
#                   max_val=max_val)
#    pylab.xlabel('Cleavage Rate (s^-1)')
#    pylab.ylabel('ATP Fluorescence Weight (AU)')
#    pylab.colorbar()


def coop(group):
    pass

def coop_adppi(group):
    slicer = slicing.Slicer.from_group(group, 'pollard_adppi_chi_squared',
                                run_parameters=['filament_tip_concentration',
                                                'cleavage_rate',
                                                'cleavage_cooperativity'],
                                table_name='cra')

    max_val = 14

    pylab.figure()

    pylab.subplot(1,3,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, max_val)

    pylab.subplot(1,3,2)
    fit_1d.simple(slicer, 'cleavage_rate',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, max_val)

    pylab.subplot(1,3,3)
    fit_1d.simple(slicer, 'cleavage_cooperativity',
                  min_color=COLORS[2][0], slice_color=COLORS[2][3],
                  logscale_x=True)
    pylab.xlabel('Cleavage Cooperativity')
    pylab.ylabel('F-ADP-Pi Fit (AU)')
    pylab.ylim(0, max_val)

    pylab.figure()

    pylab.subplot(1,2,1)
    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'filament_tip_concentration'],
                   max_val=max_val)
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()

    pylab.subplot(1,2,2)
    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'cleavage_cooperativity'],
                   max_val=max_val, logscale_y=True)
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Cleavage Cooperativity')
    pylab.colorbar()


def coop_length(group):
    slicer = slicing.Slicer.from_group(group, 'pollard_length_chi_squared',
                                run_parameters=['filament_tip_concentration',
                                                'cleavage_rate',
                                                'cleavage_cooperativity'],
                                table_name='crf')
    max_val = 0.6

    pylab.figure()

    pylab.subplot(1,3,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('F-actin Fit (AU)')
    pylab.ylim(0, max_val)

    pylab.subplot(1,3,2)
    fit_1d.simple(slicer, 'cleavage_rate',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('F-actin Fit (AU)')
    pylab.ylim(0, max_val)

    pylab.subplot(1,3,3)
    fit_1d.simple(slicer, 'cleavage_cooperativity',
                  min_color=COLORS[0][0], slice_color=COLORS[0][3],
                  logscale_x=True)
    pylab.xlabel('Cleavage Cooperativity')
    pylab.ylabel('F-actin Fit (AU)')
    pylab.ylim(0, max_val)

    pylab.figure()

    pylab.subplot(1,2,1)

    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'filament_tip_concentration'],
                   max_val=max_val)
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()

    pylab.subplot(1,2,2)

    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'cleavage_cooperativity'],
                   max_val=max_val, logscale_y=True)
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Cleavage Cooperativity')
    pylab.colorbar()


def coop_pyrene(group):
    slicer = slicing.Slicer.from_group(group, 'pollard_pyrene_chi_squared',
                                run_parameters=['filament_tip_concentration',
                                                'cleavage_rate',
                                                'cleavage_cooperativity'],
                                analysis_parameters=['atp_weight'],
                                value_type='analysis',
                                table_name='crp')
    max_val = 1
    pylab.figure()

    pylab.subplot(1,3,1)
    fit_1d.simple(slicer, 'filament_tip_concentration',
                  min_color=COLORS[1][0], slice_color=COLORS[1][3])
    pylab.xlabel('Filament Tip Concentration (uM)')
    pylab.ylabel('Pyrene Fit (AU)')
    pylab.ylim(0, max_val)

    pylab.subplot(1,3,2)
    fit_1d.simple(slicer, 'cleavage_rate',
                  min_color=COLORS[1][0], slice_color=COLORS[1][3])
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Pyrene Fit (AU)')
    pylab.ylim(0, max_val)

    pylab.subplot(1,3,3)
    fit_1d.simple(slicer, 'atp_weight',
                  min_color=COLORS[1][0], slice_color=COLORS[1][3])
    pylab.xlabel('ATP Fluorescence Weight (AU)')
    pylab.ylabel('Pyrene Fit (AU)')
    pylab.ylim(0, max_val)


    pylab.figure()

    pylab.subplot(2,2,1)
    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'filament_tip_concentration'],
                   max_val=max_val)
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()

    pylab.subplot(2,2,2)
    fit_1d.contour(slicer, abscissae_names=['atp_weight',
                                            'filament_tip_concentration'],
                   max_val=max_val)
    pylab.xlabel('ATP Fluorescence Weight (AU)')
    pylab.ylabel('Filament Tip Concentration (uM)')
    pylab.colorbar()

    pylab.subplot(2,2,3)
    fit_1d.contour(slicer, abscissae_names=['cleavage_rate',
                                            'cleavage_cooperativity'],
                   max_val=max_val, logscale_y=True)
    pylab.xlabel('Cleavage Rate (s^-1)')
    pylab.ylabel('Cleavage Cooperativity')
    pylab.colorbar()

    pylab.subplot(2,2,4)
    fit_1d.contour(slicer, abscissae_names=['atp_weight',
                                            'cleavage_cooperativity'],
                   max_val=max_val, logscale_y=True)
    pylab.xlabel('ATP Fluorescence Weight (AU)')
    pylab.ylabel('Cleavage Cooperativity')
    pylab.colorbar()

