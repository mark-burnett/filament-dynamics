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

def measurement_chi_squared(a, b, epsilon=0.01):
    '''
    Assumes equal length measurements a and b.

    Epsilon is used as the minimum squared error at each point.
    '''
    result = 0
    for ma, mb in itertools.izip(a, b):
        # Find total square error for this point
        total_square_error = 0
        if 3 == len(ma):
            total_square_error += ma[2]**2
        elif 4 == len(ma):
            total_square_error += (ma[3] - ma[2])**2

        if 3 == len(mb):
            total_square_error += mb[2]**2
        elif 4 == len(mb):
            total_square_error += (mb[3] - mb[2])**2

        if total_square_error < epsilon:
            total_square_error = epsilon

        result += (ma[2] - mb[2])**2 / total_square_error

    return result / len(a)
