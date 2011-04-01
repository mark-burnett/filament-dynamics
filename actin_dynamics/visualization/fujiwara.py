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

from actin_dynamics import database

def D_vs_concentration(session, **kwargs):
    e = session.get_experiment('fujiwara_2002')
    D_ob = e.objectives['diffusion_coefficient']
    D_s = slicing.Slicer.from_objective_bind(D_ob)

    Ds, name, concentration_mesh = D_s.minimum_values('atp_concentration')

    j_ob = e.objectives['elongation_rate']
    j_s = slicing.Slicer.from_objective_bind(j_ob)

    js, name, concentration_mesh = j_s.minimum_values('atp_concentration')

    pylab.figure()
    pylab.subplot(2,1,1)
    measurements.line((concentration_mesh[0], Ds), **kwargs)
    pylab.ylabel('Tip Diffusion Coefficient (mon**2 /s)')

    pylab.subplot(2,1,2)
    zero_concentrations = [concentration_mesh[0][0], concentration_mesh[0][-1]]
    zero_values = [0, 0]

    measurements.line((zero_concentrations, zero_values))
    measurements.line((concentration_mesh[0], js), **kwargs)
    pylab.ylabel('Elongation Rate (mon /s )')
    pylab.xlabel('[G-ATP-actin] (uM)')
