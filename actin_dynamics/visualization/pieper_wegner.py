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

import operator

import scipy.interpolate
import pylab
import numpy

from . import slicing
from . import fit
from . import themes
from . import measurements

from actin_dynamics.factories import bindings
import actin_dynamics.numerical.measurements
from actin_dynamics import numerical

def pi_session(session):
    # Release Cooperativity
    best_cooperativity = combined_pi(session, logscale_x=True, logscale_y=True)
    side_by_side_pyrene(session, parameter_name='release_cooperativity',
                        x_label='Release Cooperativity', x_scale=1,
                        logscale_x=True)

    # Release Rate
    combined_pi(session, parameter_name='release_rate',
                x_label='Release Rate (s^-1)')
    side_by_side_pyrene(session, parameter_name='release_rate',
                        x_label='Release Rate (s^-1)', x_scale=1)

    # Contours
    contour_pi(session)

    # Timecourses for all minima!
    minima_timecourses_pi(session)


def side_by_side_pyrene(session, parameter_name='filament_tip_concentration',
                        x_label='Filament Tip Concentration (nM)', x_scale=1000,
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
                 scale_x=x_scale,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_light', 'simulation_line'))
    fit.plot_min(s100brooks, parameter_name,
                 scale_x=x_scale,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_dark', 'simulation_line'))
    if not logscale_y:
        pylab.ylim(0, worst_fit)
    else:
        pylab.ylim(None, worst_fit)
    pylab.xlabel(x_label)
    pylab.ylabel('Quality of Fit (AU)')
    pylab.title('100% G-ATP-actin')


    pylab.subplot(1,3,2)
    fit.plot_min(s90flat,   parameter_name,
                 scale_x=x_scale,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_light', 'simulation_line'))
    fit.plot_min(s90brooks, parameter_name,
                 scale_x=x_scale,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_dark', 'simulation_line'))
    if not logscale_y:
        pylab.ylim(0, worst_fit)
    else:
        pylab.ylim(None, worst_fit)
    pylab.xlabel(x_label)
    pylab.title('90% G-ATP-actin')


    pylab.subplot(1,3,3)
    fit.plot_min(s50flat,   parameter_name,
                 scale_x=x_scale,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_light', 'simulation_line'))
    fit.plot_min(s50brooks, parameter_name,
                 scale_x=x_scale,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 **theme('pyrene_dark', 'simulation_line'))
    if not logscale_y:
        pylab.ylim(0, worst_fit)
    else:
        pylab.ylim(None, worst_fit)
    pylab.xlabel(x_label)
    pylab.title('50% G-ATP-actin')

    print 'Best values for', x_label
    print '100%% ATP: flat -> %s, brooks -> %s' % (
            x_scale * s100flat.get_best_parameters()[parameter_name],
            x_scale * s100brooks.get_best_parameters()[parameter_name])

    print ' 90%% ATP: flat -> %s, brooks -> %s' % (
            x_scale * s90flat.get_best_parameters()[parameter_name],
            x_scale * s90brooks.get_best_parameters()[parameter_name])

    print ' 50%% ATP: flat -> %s, brooks -> %s' % (
            x_scale * s50flat.get_best_parameters()[parameter_name],
            x_scale * s50brooks.get_best_parameters()[parameter_name])


def combined_pi(session, parameter_name='release_cooperativity',
                x_label='Release Cooperativity',
                theme=None, logscale_x=False, logscale_y=False):
    e100 = session.get_experiment('pieper_wegner_100')
    e90  = session.get_experiment('pieper_wegner_90')
    e50  = session.get_experiment('pieper_wegner_50')

    s100 = slicing.Slicer.from_objective_bind(e100.objectives['pieper_wegner_pi_fit'])
    s90  = slicing.Slicer.from_objective_bind( e90.objectives['pieper_wegner_pi_fit'])
    s50  = slicing.Slicer.from_objective_bind( e50.objectives['pieper_wegner_pi_fit'])

    worst_fit = max(s100.get_worst_value(),
                    s90.get_worst_value(),
                    s50.get_worst_value())

    if not theme:
        theme = themes.Theme()

    pylab.figure()

    fit.plot_min(s100, parameter_name,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 label='100% ATP',
                 **theme('pi_light1', 'simulation_line'))

    fit.plot_min(s90, parameter_name,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 label='90% ATP',
                 **theme('pi_light2', 'simulation_line'))

    fit.plot_min(s50, parameter_name,
                 logscale_x=logscale_x, logscale_y=logscale_y,
                 label='50% ATP',
                 **theme('pi_light3', 'simulation_line'))

    best = fit.averaged_min([s100, s90, s50], parameter_name,
                            logscale_x=logscale_x, logscale_y=logscale_y,
                            label='Average',
                            **theme('pi_dark', 'simulation_line'))

    if not logscale_y:
        pylab.ylim(0, worst_fit)
    else:
        pylab.ylim(None, worst_fit)

    pylab.legend(loc=4)
    pylab.xlabel(x_label)
    pylab.ylabel('Quality of Fit (AU)')

    print '100%% ATP:', s100.get_best_parameters()[parameter_name]
    print ' 90%% ATP:',  s90.get_best_parameters()[parameter_name]
    print ' 50%% ATP:',  s50.get_best_parameters()[parameter_name]
    print 'Average:  ', best

    return best

def contour_pi(session, logscale_x=True, logscale_y=True, logscale_z=True):
    e100 = session.get_experiment('pieper_wegner_100')
    e90  = session.get_experiment('pieper_wegner_90')
    e50  = session.get_experiment('pieper_wegner_50')

    s100 = slicing.Slicer.from_objective_bind(e100.objectives['pieper_wegner_pi_fit'])
    s90  = slicing.Slicer.from_objective_bind( e90.objectives['pieper_wegner_pi_fit'])
    s50  = slicing.Slicer.from_objective_bind( e50.objectives['pieper_wegner_pi_fit'])

    pylab.figure()

    pylab.subplot(2, 2, 1)
    fit.contour(s100, 'release_cooperativity', 'release_rate',
                logscale_x=logscale_x, logscale_y=logscale_y,
                logscale_z=logscale_z)
    pylab.title('100% ATP')
    pylab.subplot(2, 2, 2)
    fit.contour(s90, 'release_cooperativity', 'release_rate',
                logscale_x=logscale_x, logscale_y=logscale_y,
                logscale_z=logscale_z)
    pylab.title('90% ATP')
    pylab.subplot(2, 2, 3)
    fit.contour(s50, 'release_cooperativity', 'release_rate',
                logscale_x=logscale_x, logscale_y=logscale_y,
                logscale_z=logscale_z)
    pylab.title('50% ATP')

    pylab.subplot(2, 2, 4)
    fit.averaged_contour([s100, s90, s50],
                         'release_cooperativity', 'release_rate',
                         logscale_x=logscale_x, logscale_y=logscale_y,
                         logscale_z=logscale_z)
    pylab.title('Average')


def timecourse(run, final_pyrene_value=None, with_date=True, theme=None):
    if not theme:
        theme = themes.Theme()

    pylab.figure()
    # unweighted f-actin
    total_factin = numerical.measurements.add([
        run.analyses['pyrene_ATP'],
        run.analyses['pyrene_ADPPi'],
        run.analyses['pyrene_ADP']])

    factin_concentration = numerical.measurements.scale(total_factin,
            run.all_parameters['filament_tip_concentration'])

    measurements.plot_smooth(factin_concentration, label='F-actin',
                             **theme('factin_dark', 'simulation_line'))

    # pi + data
    measurements.plot_smooth(run.analyses['Pi'], label='[Pi] Simulation',
                             **theme('pi_dark', 'simulation_line'))
    pi_data = run.experiment.objectives['pieper_wegner_pi_fit'].measurement
    measurements.plot_scatter(pi_data, label='[Pi] Data',
                              **theme('pi_light', 'data_points'))

    # both pyrene intensities + data
    flat_bind   = run.experiment.objectives['flat_pyrene_fit']
    brooks_bind = run.experiment.objectives['brooks_pyrene_fit']

    pyrene_data = brooks_bind.measurement
    if final_pyrene_value:
        scale_factor = float(final_pyrene_value) / pyrene_data[1][-1]
    else:
        scale_factor = 1
    scaled_pyrene_data = numerical.measurements.scale(pyrene_data, scale_factor)

    measurements.plot_smooth(scaled_pyrene_data, label='Pyrene Data',
                             **theme('pyrene_light3', 'data_line'))

    flat_objective = bindings.db_single(flat_bind, run.all_parameters)
    flat_fit, flat_measurement = flat_objective.fit_measurement(run,
            scaled_pyrene_data)
    measurements.plot_smooth(flat_measurement, label='Flat Pyrene Simulation',
                             **theme('pyrene_light1', 'simulation_line'))

    brooks_objective = bindings.db_single(brooks_bind, run.all_parameters)
    brooks_fit, brooks_measurement = brooks_objective.fit_measurement(run,
            scaled_pyrene_data)
    measurements.plot_smooth(brooks_measurement,
                             label='Brooks Pyrene Simulation',
                             **theme('pyrene_dark', 'simulation_line'))

    # limits
    pylab.xlim(0, 600)
    pylab.ylim(0, None)
    pylab.legend(loc=4)



class Simple2dSpliner(object):
    def __init__(self, x, y, z, epsilon=1e-3, *args, **kwargs):
        self.x, self.y = numpy.meshgrid(x, y)
        self.z = numpy.reshape(z, reduce(operator.mul, z.shape))

        weights = numpy.ones(self.z.shape) * epsilon
        self.tck = scipy.interpolate.bisplrep(self.x, self.y, self.z, w=weights,
                                              nxest=len(x), nyest=len(y),
                                              *args, **kwargs)

    def __call__(self, x, y, derivative=0):
        return scipy.interpolate.bisplev(x, y, self.tck,
                                         dx=int(derivative), dy=int(derivative))

def minima_timecourses_pi(session, scale=4, threshold=None,
                          x_name='release_cooperativity',
                          y_name='release_rate'):
    e100 = session.get_experiment('pieper_wegner_100')
    e90  = session.get_experiment('pieper_wegner_90')
    e50  = session.get_experiment('pieper_wegner_50')

    s100 = slicing.Slicer.from_objective_bind(e100.objectives['pieper_wegner_pi_fit'])
    s90  = slicing.Slicer.from_objective_bind( e90.objectives['pieper_wegner_pi_fit'])
    s50  = slicing.Slicer.from_objective_bind( e50.objectives['pieper_wegner_pi_fit'])

    # Get z values
    all_zs = []
    for slicer in [s100, s90, s50]:
        z, xy_names, xy_meshes = slicer.minimum_values(x_name, y_name)
        x_mesh, y_mesh = xy_meshes
        all_zs.append(z)

    # Average z values
    averaged_zs = reduce(operator.add, all_zs) / len(all_zs)

    # Calculate the second derivative everywhere.
    spliner = Simple2dSpliner(x_mesh, y_mesh, averaged_zs)
    second_derivatives = spliner(x_mesh, y_mesh, derivative=2)

    # Flatten second derivative.
    second_derivatives = numpy.reshape(second_derivatives,
            reduce(operator.mul, second_derivatives.shape))

    mag_sd = numpy.abs(second_derivatives)
    sdmin = numpy.min(mag_sd)
    sd_index = numpy.argmin(mag_sd)

    if threshold is None:
        threshold = scale * sdmin

    flat_average =  numpy.reshape(averaged_zs,
            reduce(operator.mul, averaged_zs.shape))

    print 'Sharpest minimum:', sdmin, 'at index:', sd_index, 'value:', flat_average[sd_index]
    print '%s minima below threshold = %s.' % (sum(mag_sd < threshold),
                                               threshold)
