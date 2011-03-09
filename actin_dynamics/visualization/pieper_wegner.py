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

from . import slicing
from . import fit
from . import themes

def side_by_side_pyrene(session, parameter_name='filament_tip_concentration',
                        theme=None, logscale_x=False, logscale_y=False):
    '''
    Plot pyrene fits for flat and brooks's coefficients for all 3 experiments.
    '''
    e100 = session.get_experiment('pieper_wegner_100')
    e90  = session.get_experiment('pieper_wegner_90')
    e50  = session.get_experiment('pieper_wegner_50')

    s100flat   = slicing.Slicer.from_objective_bind(e100.objectives['flat_pyrene_fit'])
    s100brooks = slicing.Slicer.from_objective_bind(e100.objectives['brooks_pyrene_fit'])

    s90flat    = slicing.Slicer.from_objective_bind(e90.objectives['flat_pyrene_fit'])
    s90brooks  = slicing.Slicer.from_objective_bind(e90.objectives['brooks_pyrene_fit'])

    s50flat    = slicing.Slicer.from_objective_bind(e50.objectives['flat_pyrene_fit'])
    s50brooks  = slicing.Slicer.from_objective_bind(e50.objectives['brooks_pyrene_fit'])


    worst_fit = max(s100flat.get_worst_value(),
                    s100brooks.get_worst_value(),
                    s90flat.get_worst_value(),
                    s90brooks.get_worst_value(),
                    s50flat.get_worst_value(),
                    s50brooks.get_worst_value())

    if not theme:
        theme = themes.Theme()

    pylab.figure()

    pylab.subplot(1,3,1)
    fit.plot_min(s100flat,   parameter_name,
                 scale_x=1000,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_light', 'simulation_line'))
    fit.plot_min(s100brooks, parameter_name,
                 scale_x=1000,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_dark', 'simulation_line'))
    if not logscale_y:
        pylab.ylim(0, worst_fit)
    else:
        pylab.ylim(None, worst_fit)
    pylab.xlabel('Filament Tip Concentration (nM)')
    pylab.ylabel('Quality of Fit (AU)')
    pylab.title('100% G-ATP-actin')


    pylab.subplot(1,3,2)
    fit.plot_min(s90flat,   parameter_name,
                 scale_x=1000,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_light', 'simulation_line'))
    fit.plot_min(s90brooks, parameter_name,
                 scale_x=1000,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_dark', 'simulation_line'))
    if not logscale_y:
        pylab.ylim(0, worst_fit)
    else:
        pylab.ylim(None, worst_fit)
    pylab.xlabel('Filament Tip Concentration (nM)')
    pylab.title('90% G-ATP-actin')


    pylab.subplot(1,3,3)
    fit.plot_min(s50flat,   parameter_name,
                 scale_x=1000,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_light', 'simulation_line'))
    fit.plot_min(s50brooks, parameter_name,
                 scale_x=1000,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_dark', 'simulation_line'))
    if not logscale_y:
        pylab.ylim(0, worst_fit)
    else:
        pylab.ylim(None, worst_fit)
    pylab.xlabel('Filament Tip Concentration (nM)')
    pylab.title('50% G-ATP-actin')

    print '100%% ATP: flat -> %s, brooks -> %s' % (
            1000 * s100flat.get_best_parameters()[parameter_name],
            1000 * s100brooks.get_best_parameters()[parameter_name])

    print ' 90%% ATP: flat -> %s, brooks -> %s' % (
            1000 * s90flat.get_best_parameters()[parameter_name],
            1000 * s90brooks.get_best_parameters()[parameter_name])

    print ' 50%% ATP: flat -> %s, brooks -> %s' % (
            1000 * s50flat.get_best_parameters()[parameter_name],
            1000 * s50brooks.get_best_parameters()[parameter_name])
