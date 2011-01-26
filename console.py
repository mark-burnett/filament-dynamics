#!/usr/bin/env ipython
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

from actin_dynamics import analysis
from actin_dynamics import visualization
from actin_dynamics import io

import numpy
import pylab

#atp_weights = numpy.linspace(0.2, 0.7, 10)
atp_weights = [0.2, 0.7]
sims = io.compressed.read_object('results/pollard/combined.sim')
pyrene_data, adppi_data = analysis.pollard.get_data()
