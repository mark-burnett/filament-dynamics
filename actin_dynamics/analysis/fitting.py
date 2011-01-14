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

import itertools
import math

from actin_dynamics import vectorize

def measurement_chi_squared(a, b, minimum_error=0.001):
    at, av, ae = a
    bt, bv, be = b

    errors = [0 for a in av]
    if 3 == len(a):
        errors = vectorize.add(errors, [ax**2 for ax in ae])
    if 3 == len(b):
        errors = vectorize.add(errors, [bx**2 for bx in be])

    for i, e in enumerate(errors):
        if e < minimum_error:
            errors[i] = 1

    return sum((ax - bx)**2 / ex
               for ax, bx, ex in itertools.izip(av, bv, errors))

def measurement_other(a, b, minimum_error=0.0001):
    at, av, ae = a
    bt, bv, be = b

    errors = [0 for a in av]
    if 3 == len(a):
        errors = vectorize.add(errors, [ax**2 for ax in ae])
    if 3 == len(b):
        errors = vectorize.add(errors, [bx**2 for bx in be])

    for i, e in enumerate(errors):
        if e < minimum_error:
            errors[i] = 1

    return 2 * sum((ax - bx)**2 / abs(ax + bx) / math.sqrt(ex)
                   for ax, bx, ex in itertools.izip(ax, bx, ex))
