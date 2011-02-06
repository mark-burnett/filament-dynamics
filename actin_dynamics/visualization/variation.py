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

def run_val_vs_par(group, abscissa=None, ordinate=None, label=None, theme=None):
    x, y = slicing.rv_rp_reduce(group, parameter_name=abscissa,
                                value_name=ordinate)

    measurements.plot_smooth((x, y), label=label, **theme(x, y, abscissa))
