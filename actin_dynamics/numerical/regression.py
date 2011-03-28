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

import numpy

from scipy import polyfit
from scipy.optimize import fmin

from . import residuals

from actin_dynamics import logger
log = logger.getLogger(__file__)

def fit_gaussian(x_mesh, y_mesh):
    total_y = sum(y_mesh)
    mean = sum(x * y for x, y in itertools.izip(x_mesh, y_mesh)) / total_y
    variance = sum(y * (x - mean)**2
                   for x, y in itertools.izip(x_mesh, y_mesh)) / total_y
    return mean, variance #, magnitude


def fit_line(x_mesh, y_mesh):
    return polyfit(x_mesh, y_mesh, 1)

def fit_zero_line(x_mesh, y_mesh, residual=residuals.naked_chi_squared):
    intercept = y_mesh[0]
    x = numpy.array(x_mesh)
    guess = (y_mesh[-1] - y_mesh[0]) / (x_mesh[-1] - x_mesh[0])

    def fit_func(slope):
        line = x * slope[0] + intercept
        return residual([None, y_mesh], [None, line])

    fit_results = fmin(fit_func, guess, disp=False, full_output=True)
    return fit_results[0][0]
