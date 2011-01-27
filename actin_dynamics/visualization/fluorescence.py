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

from actin_dynamics import analysis
from . import pollard

def plot_ranked_object(ranked_object):
    parameter_set, atp_weight = ranked_object.parameters
    pyrene_data, adppi_data = analysis.pollard.get_data()
    analysis.pollard.pyrene_fit(parameter_set, pyrene_data,
                                atp_weight=atp_weight, write=True)
    pollard.plot_full_par_set(parameter_set)

def fitness_vectors(atp_weights, fitness_vectors):
    pylab.figure()
    residuals = numpy.array(fitness_vectors).transpose()
    for row in residuals:
        row_min = min(row)
        row /= row_min
        row -= 1
        pylab.scatter(atp_weights, row)
