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

from . import measurements
from . import slicing

from actin_dynamics import database

def D_vs_concentration(session, **kwargs):
    ob = session.get_experiment('fujiwara_2002').objectives['diffusion_coefficient']
    s = slicing.Slicer.from_objective_bind(ob)

    Ds, name, concentration_mesh = s.minimum_values('atp_concentration')

    measurements.line((concentration_mesh[0], Ds), **kwargs)
