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

# This file contains some pure python functional replacements for e.g. numpy.

import itertools
import math

def add(a, b):
    result = []
    for ax, bx in itertools.izip(a, b):
        result.append(ax + bx)

    return result


def arange(min_value, max_value, dx):
    result = []
    value = min_value
    while value < max_value:
        result.append(value)
        value += dx
    return result

def linspace(min_value, max_value, num_points):
    if num_points > 1:
        dx = float(max_value - min_value) / (num_points - 1)
        return [min_value + i * dx for i in xrange(num_points)]
    else:
        return [min_value]


def std(values, mean):
    return math.sqrt(sum((v - mean)**2 for v in values) / len(values))
