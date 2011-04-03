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

from . import interpolation

def zero_crossings(x, y, interpolate=True):
    zero_crossings = numpy.where(numpy.diff(numpy.sign(y)))[0]

    if not interpolate:
        return [x[i] for i in zero_crossings]

    results = []
    for i in zero_crossings:
        results.append(interpolation.linear_project(y[i], x[i],
                                                    y[i+1], x[i+1],
                                                    0))
    return results
