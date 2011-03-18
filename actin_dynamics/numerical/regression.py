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

import itertools
from scipy import polyfit

def fit_gaussian(x_mesh, y_mesh):
    bin_size = x_mesh[1] - x_mesh[0]
    total_y = sum(y_mesh) * bin_size
    mean = sum(x * y for x, y in itertools.izip(x_mesh, y_mesh)) * bin_size / total_y

    variance = sum(y * (x - mean)**2
                   for x, y in itertools.izip(x_mesh, y_mesh)) * bin_size / total_y
    return mean, variance


def fit_line(x_mesh, y_mesh):
    return polyfit(x_mesh, y_mesh, 1)
