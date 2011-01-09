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

from . import utils

def plot_scatter_measurement(measurement, color='blue', fmt='o', **kwargs):
    error_bars = utils.get_error_bars(measurement)
    times, values = measurement[:2]

    if error_bars:
        pylab.errorbar(times, values, yerr=error_bars, color=color, fmt=fmt,
                       **kwargs)
    else:
        pylab.scatter(times, values, color=color, **kwargs)

def plot_smooth_measurement(measurement, color='black', fill_alpha=0.5,
                            linestyle='solid', **kwargs):
    bounds = utils.get_bounds(measurement)
    times, values = measurement[:2]

    if bounds:
        pylab.fill_between(times, bounds[0], bounds[1],
                           color=color, alpha=fill_alpha, **kwargs)

    pylab.plot(times, values, color=color, linestyle=linestyle, **kwargs)
