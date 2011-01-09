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

import itertools

def measurement_chi_squared(a, b, minimum_error=0.001):
    av = numpy.array(a[1])
    bv = numpy.array(b[1])

    errors = numpy.zeros(len(av))
    if 3 == len(a):
        errors += numpy.power(a[2], 2)
    elif 4 == len(a):
        errors += numpy.power(numpy.array(a[3]) - numpy.array(a[2]), 2)
    if 3 == len(b):
        errors += numpy.power(b[2], 2)
    elif 4 == len(b):
        errors += numpy.power(numpy.array(b[3]) - numpy.array(b[2]), 2)

    for i, e in enumerate(errors):
        if e < minimum_error:
            errors[i] = 1

    return sum(numpy.power(av-bv,2) / errors)

def measurement_other(a, b, minimum_error=0.001):
    av = numpy.array(a[1])
    bv = numpy.array(b[1])

    errors = numpy.array([minimum_error for v in av])
#    errors = numpy.zeros(len(av))
    if 3 == len(a):
        errors += numpy.power(a[2], 2)
    elif 4 == len(a):
        errors += numpy.power(numpy.array(a[3]) - numpy.array(a[2]), 2)
    if 3 == len(b):
        errors += numpy.power(b[2], 2)
    elif 4 == len(b):
        errors += numpy.power(numpy.array(b[3]) - numpy.array(b[2]), 2)

#    for i, e in enumerate(errors):
#        if e < minimum_error:
#            errors[i] = 1

    return 2 * sum(numpy.power(av-bv,2) / sum(av + bv) / numpy.sqrt(errors))
