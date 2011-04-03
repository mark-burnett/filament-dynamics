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

import pylab

from . import measurements
from . import slicing

from actin_dynamics.numerical.zero_crossings import zero_crossings

def elongation_rate_vs_conc(session, **kwargs):
    ob = session.get_experiment('critical_concentration').objectives['elongation_rate']

    s = slicing.Slicer.from_objective_bind(ob)

    rs, names, concentration_mesh = s.minimum_values('atp_concentration')

    zero_concentrations = [concentration_mesh[0][0], concentration_mesh[0][-1]]
    zero_values = [0, 0]

    measurements.line((concentration_mesh[0], rs), **kwargs)
    measurements.line((zero_concentrations, zero_values))
    pylab.xlabel('[G-ATP-actin] (uM)')
    pylab.ylabel('Average Elongation Rate (mon / s)')

def get_cc(experiment):
    ob = experiment.objectives['elongation_rate']

    s = slicing.Slicer.from_objective_bind(ob)

    rs, names, concentration_mesh = s.minimum_values('atp_concentration')
    cc = zero_crossings(concentration_mesh[0], rs)[0]

    return cc
