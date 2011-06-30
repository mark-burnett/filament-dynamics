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

def bar(measurement, color='black', **kwargs):
    centers, values, errors = measurement

    pylab.bar(centers, values, width=width, align='center', color=color,
              **kwargs)

def line(measurement, color='black', linestyle='solid',
         line_alpha=1, fill_alpha=0.5, x_scale=None, **kwargs):
    bounds = get_bounds(measurement)
    times, values = measurement[:2]
    if x_scale:
        times = [t * x_scale for t in times]

    if bounds:
        pylab.fill_between(times, bounds[0], bounds[1],
                           color=color, alpha=fill_alpha, **kwargs)

    pylab.plot(times, values, color=color, linestyle=linestyle,
               alpha=line_alpha, **kwargs)
    pylab.xlim(times[0], times[-1])


def scatter(measurement, color='black', fmt='o', **kwargs):
    error_bars = get_error_bars(measurement)
    times, values = measurement[:2]

    if error_bars:
        return pylab.errorbar(times, values, yerr=error_bars, color=color,
                              fmt=fmt, **kwargs)
    else:
        return pylab.scatter(times, values, color=color, **kwargs)


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
