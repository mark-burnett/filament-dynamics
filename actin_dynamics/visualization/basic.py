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
import numpy

from . import utils

def plot_scatter_measurement(measurement, color='blue', fmt='o', **kwargs):
    error_bars = utils.get_error_bars(measurement)
    times, values = measurement[:2]

    if error_bars:
        return pylab.errorbar(times, values, yerr=error_bars, color=color,
                              fmt=fmt, **kwargs)
    else:
        return pylab.scatter(times, values, color=color, **kwargs)

def plot_smooth_measurement(measurement, color='black', fill_alpha=0.5,
                            linestyle='solid', line_alpha=1, **kwargs):
    bounds = utils.get_bounds(measurement)
    times, values = measurement[:2]

    if bounds:
        pylab.fill_between(times, bounds[0], bounds[1],
                           color=color, alpha=fill_alpha, **kwargs)

    return pylab.plot(times, values, color=color, linestyle=linestyle,
                      alpha=line_alpha, **kwargs)

def plot_contour(x_values, y_values, z_values, reduction_axis=None,
                 xlabel=None, ylabel=None,
                 logscale_x=False, logscale_y=False, logscale_z=False,
                 transpose=True):
    if xlabel:
        pylab.xlabel(xlabel)
    if ylabel:
        pylab.ylabel(ylabel)
    reduced_z = z_values
    if reduction_axis is not None:
        reduced_z = z_values.min(reduction_axis)
    if logscale_z:
        reduced_z = numpy.log10(reduced_z)

    if transpose:
        reduced_z = reduced_z.transpose()


    pylab.contourf(x_values, y_values, reduced_z, cmap=pylab.cm.PRGn)
    pylab.colorbar()

    axes = pylab.gca()
    if logscale_x:
        axes.set_xscale('log')
    if logscale_y:
        axes.set_yscale('log')

    pylab.xlim(x_values[0], x_values[-1])
    pylab.ylim(y_values[0], y_values[-1])
