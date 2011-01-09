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

import numpy
import pylab

def plot_scatter_measurement(measurement, color='blue', fmt='o'):
    error_bars = get_error_bars(measurement)
    times, values = measurement[:2]

    if error_bars:
        pylab.errorbar(times, values, yerr=error_bars, color=color, fmt=fmt)
    else:
        pylab.scatter(times, values, color=color, fmt=fmt)

def plot_smooth_measurement(measurement, color='blue', fill_alpha=0.5):
    bounds = get_bounds(measurement)
    times, values = measurement[:2]

    if bounds:
        pylab.fill_between(times, bounds[0], bounds[1],
                           color=color, alpha=fill_alpha)

    pylab.plot(times, values, color=color)

def get_bounds(measurement):
    if 3 == len(measurement):
        avg = numpy.array(measurement[1])
        err = numpy.array(measurement[2])
        return avg - err, avg + err

    if 4 == len(measurement):
        return measurement[2], measurement[3]

    return False

def get_error_bars(measurement):
    if 3 == len(measurement):
        return measurement[2]

    if 4 == len(measurement):
        avg = numpy.array(measurement[1])
        lower = numpy.array(measurement[2])
        upper = numpy.array(measurement[3])
        return avg - lower, upper - avg

    return False
