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

import math

import numpy


def standard_error_of_mean(values, scale_by=None, add=0):
    '''
    Compute the mean and the standard error of the mean for values.
    '''
    length = len(values)
    sqrt_N = math.sqrt(length)

    if scale_by:
        adjusted_values = [v * scale_by for v in values]
    else:
        adjusted_values = values

    mean = numpy.mean(adjusted_values)
    error = numpy.std(adjusted_values) / sqrt_N

    if add:
        mean += add
    return mean, error
