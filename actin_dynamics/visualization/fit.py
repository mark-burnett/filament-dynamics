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

import numpy
import pylab
import matplotlib.ticker

import itertools
import operator

import actin_dynamics.numerical.measurements
from actin_dynamics import numerical

from . import measurements
from . import themes

import pprint

def plot_slice(slicer, abscissae_name, slice_point={},
               logscale_x=False, logscale_y=False, **kwargs):
    y, junk, x = slicer.slice(**slice_point)

    measurements.plot_smooth((x[0], y), **kwargs)

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')
    pylab.xlim(x[0][0], x[0][-1])


def plot_min(slicer, abscissae_name, scale_x=1,
             logscale_x=False, logscale_y=False, **kwargs):
    y, junk, x = slicer.minimum_values(abscissae_name)
    scaled_x = [xv * scale_x for xv in x[0]]

    measurements.plot_smooth((scaled_x, y), **kwargs)

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')
    pylab.xlim(x[0][0] * scale_x, x[0][-1] * scale_x)

def averaged_min(slicers, abscissae_name, scale_x=1,
                 logscale_x=False, logscale_y=False, **kwargs):
    all_measurements = []
    for slicer in slicers:
        y, junk, x = slicer.minimum_values(abscissae_name)
        e = [0 for yv in y]
        scaled_x = [xv * scale_x for xv in x[0]]
        all_measurements.append((scaled_x, y, e))

    average_measurement = numerical.measurements.scale(
            numerical.measurements.add(all_measurements[:2]),
            1.0 / len(all_measurements))

    measurements.plot_smooth(average_measurement, **kwargs)

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')
    pylab.xlim(average_measurement[0][0], average_measurement[0][-1])

    best_y = None
    best_x = None
    for x, y, e in itertools.izip(*average_measurement):
        if best_y is None or y < best_y:
            best_x = x
            best_y = y
    return best_x


def slice_and_min(slicer=None, abscissa_name=None, theme=None,
                  min_attributes=[], slice_attributes=[], shared_attributes=[],
                  logscale_x=False, logscale_y=False,
                  x_lower_bound=None, x_upper_bound=None,
                  y_lower_bound=None, y_upper_bound=None,
                  **fixed_values):
    # Determine fixed point for slice.
    best_pars, best_id = slicer.get_best_parameters()
    fixed_point = dict((n, x) for n, x in best_pars.iteritems()
                       if n != abscissa_name)
    if fixed_values:
        fixed_point.update(fixed_values)

    print 'Best parameters:'
    pprint.pprint(best_pars)
    print 'Best objective id:', best_id
    print 'Slice fixed point:'
    pprint.pprint(fixed_point)

    sl_y,  junk_name, sl_x  = slicer.slice(**fixed_point)
    min_y, junk_name, min_x = slicer.minimum_values(abscissa_name)

    if not theme:
        theme = themes.Theme()
    measurements.plot_smooth((min_x[0], min_y),
                             **theme(*(min_attributes + shared_attributes)))
    measurements.plot_smooth((sl_x[0], sl_y),
                             **theme(*(slice_attributes + shared_attributes)))

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')

    # Set automatic bounds.
    if x_lower_bound is None:
        x_lower_bound = min_x[0][0]
    if x_upper_bound is None:
        x_upper_bound = min_x[0][-1]

    if y_lower_bound is None:
        y_lower_bound = min(min(min_y), min(sl_y))
    if y_upper_bound is None:
        y_upper_bound = max(max(min_y), max(sl_y))

    pylab.xlim(x_lower_bound, x_upper_bound)
    pylab.ylim(y_lower_bound, y_upper_bound)


def contour(slicer, x_name, y_name,
            logscale_x=False, logscale_y=False, logscale_z=False,
            x_lower_bound=None, x_upper_bound=None,
            y_lower_bound=None, y_upper_bound=None,
            z_lower_bound=None, z_upper_bound=None,
            scale_x=1, colorbar=True):
    # Get z values
    z, xy_names, xy_meshes = slicer.minimum_values(x_name, y_name)
    x_mesh, y_mesh = xy_meshes
    scaled_x = [x * scale_x for x in x_mesh]

    # Transform z (for matplotlib's convention) and take log.
    if logscale_z:
        plot_z = numpy.log10(z).transpose()
    else:
        plot_z = z.transpose()

#    locator = matplotlib.ticker.MaxNLocator(10)
#    locator.create_dummy_axis()
#    if logscale_z:
#        if z_lower_bound and z_upper_bound:
#            locator.set_bounds(numpy.log10(z_lower_bound),
#                               numpy.log10(z_upper_bound))
#    else:
#        if z_lower_bound or z_upper_bound:
#            locator.set_bounds(z_lower_bound, z_upper_bound)
#    levels = locator()

    plot_x, plot_y = numpy.meshgrid(scaled_x, y_mesh)
    pylab.contourf(plot_x, plot_y, plot_z, cmap=pylab.cm.PRGn)
#    pylab.contourf(plot_x, plot_y, plot_z, levels, cmap=pylab.cm.PRGn)

    # Set automatic bounds.
    if x_lower_bound is None:
        x_lower_bound = scaled_x[0]
    if x_upper_bound is None:
        x_upper_bound = scaled_x[-1]

    if y_lower_bound is None:
        y_lower_bound = y_mesh[0]
    if y_upper_bound is None:
        y_upper_bound = y_mesh[-1]

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')

    pylab.xlim(x_lower_bound, x_upper_bound)
    pylab.ylim(y_lower_bound, y_upper_bound)

    if colorbar:
        pylab.colorbar()


def averaged_contour(slicers, x_name, y_name,
                     logscale_x=False, logscale_y=False, logscale_z=False,
                     x_lower_bound=None, x_upper_bound=None,
                     y_lower_bound=None, y_upper_bound=None,
                     z_lower_bound=None, z_upper_bound=None,
                     scale_x=1,
                     colorbar=True):
    # Get z values
    all_zs = []
    for slicer in slicers:
        z, xy_names, xy_meshes = slicer.minimum_values(x_name, y_name)
        x_mesh, y_mesh = xy_meshes
        scaled_x = [x * scale_x for x in x_mesh]
        all_zs.append(z)

    # Average z values
    averaged_zs = reduce(operator.add, all_zs) / len(all_zs)

    # Transform z (for matplotlib's convention) and take log.
    if logscale_z:
        plot_z = numpy.log10(averaged_zs).transpose()
    else:
        plot_z = averaged_zs.transpose()

#    locator = matplotlib.ticker.MaxNLocator(10)
#    locator.create_dummy_axis()
#    if logscale_z:
#        if z_lower_bound and z_upper_bound:
#            locator.set_bounds(numpy.log10(z_lower_bound),
#                               numpy.log10(z_upper_bound))
#    else:
#        locator.set_bounds(z_lower_bound, z_upper_bound)
#    levels = locator()

    plot_x, plot_y = numpy.meshgrid(scaled_x, y_mesh)
    pylab.contourf(plot_x, plot_y, plot_z, cmap=pylab.cm.PRGn)
#    pylab.contourf(plot_x, plot_y, plot_z, levels, cmap=pylab.cm.PRGn)

    # Set automatic bounds.
    if x_lower_bound is None:
        x_lower_bound = scaled_x[0]
    if x_upper_bound is None:
        x_upper_bound = scaled_x[-1]

    if y_lower_bound is None:
        y_lower_bound = y_mesh[0]
    if y_upper_bound is None:
        y_upper_bound = y_mesh[-1]

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')

    pylab.xlim(x_lower_bound, x_upper_bound)
    pylab.ylim(y_lower_bound, y_upper_bound)

    if colorbar:
        pylab.colorbar()
