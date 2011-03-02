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
import matplotlib.ticker

from .. import themes
from .. import measurements

def plot_slice(slicer, abscissae_name, slice_point={},
               logscale_x=False, logscale_y=False, **kwargs):
    y, junk, x = slicer.slice(**slice_point)

    measurements.plot_smooth((x[0], y), **kwargs)

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')
    pylab.xlim(x[0][0], x[0][-1])


def plot_min(slicer, abscissae_name,
             logscale_x=False, logscale_y=False, **kwargs):
    y, junk, x = slicer.minimum_values(abscissae_name)

    measurements.plot_smooth((x[0], y), **kwargs)

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')
    pylab.xlim(x[0][0], x[0][-1])



def simple(slicer, abscissa_name, min_color=None, slice_color=None,
           logscale_x=False, logscale_y=False,
           **kwargs):

    best_pars, best_id = slicer.get_best_parameters()

    fixed_point = dict((n, x) for n, x in best_pars.iteritems()
                       if n != abscissa_name)

    if kwargs:
        fixed_point.update(kwargs)
    sl_y, junk_name, sl_x = slicer.slice(**fixed_point)

    min_y, junk_name, min_x = slicer.minimum_values(abscissa_name)

    measurements.plot_smooth((min_x[0], min_y), color=min_color, linewidth=2)
    measurements.plot_smooth((sl_x[0], sl_y), color=slice_color, linewidth=2)
    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')
    pylab.xlim(min_x[0][0], min_x[0][-1])

def simple_contour(values, x, y, min_val=0, max_val=1,
                   logscale_x=False, logscale_y=False, logscale_z=False):
    if logscale_z:
        values = numpy.log10(values)

    # XXX Apparently, you have to transpose stuff for matplotlib...
    values = values.transpose()
    X, Y = numpy.meshgrid(x, y)

    #locator = matplotlib.ticker.MaxNLocator(10)
    #locator.create_dummy_axis()
    #locator.set_bounds(min_val, max_val)
    #levels = locator()

    pylab.contourf(X, Y, values, cmap=pylab.cm.PRGn)
#    pylab.contourf(X, Y, values, levels, cmap=pylab.cm.PRGn)

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')

    pylab.xlim(x[0], x[-1])
    pylab.ylim(y[0], y[-1])

def contour(slicer, abscissae_names, max_val=None,
            logscale_x=False, logscale_y=False, logscale_z=False):
    values, names, meshes = slicer.minimum_values(*abscissae_names)

    if logscale_z:
        values = numpy.log10(values)

    # XXX Apparently, you have to transpose stuff for matplotlib...
    values = values.transpose()
    X, Y = numpy.meshgrid(meshes[0], meshes[1])

    locator = matplotlib.ticker.MaxNLocator(10)
    if max_val:
        locator.create_dummy_axis()
        locator.set_bounds(0, max_val)
    levels = locator()

    result = pylab.contourf(X, Y, values, levels, cmap=pylab.cm.PRGn)

    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')

    pylab.xlim(meshes[0][0], meshes[0][-1])
    pylab.ylim(meshes[1][0], meshes[1][-1])

    return result
