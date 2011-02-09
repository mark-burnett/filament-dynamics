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
import pylab

from .. import themes
from .. import measurements

def simple(slicer, abscissa_name, min_color=None, slice_color=None,
           logscale_x=False, logscale_y=False):

    best_val, all_names, best_x = slicer.minimum_values()

    fixed_point = dict((n, x) for n, x in itertools.izip(all_names, best_x)
                       if n != abscissa_name)

    min_y, junk_name, min_x = slicer.minimum_values(abscissa_name)
    sl_y, junk_name, sl_x = slicer.slice(**fixed_point)

    measurements.plot_smooth((min_x[0], min_y), color=min_color, linewidth=2)
    measurements.plot_smooth((sl_x[0], sl_y), color=slice_color, linewidth=2)
    if logscale_x:
        pylab.gca().set_xscale('log')
    if logscale_y:
        pylab.gca().set_yscale('log')
    pylab.xlim(min_x[0][0], min_x[0][-1])

def contour(slicer, abscissae_names, logscale_z=True):
    values, names, meshes = slicer.minimum_values(*abscissae_names)

    if logscale_z:
        values = numpy.log10(values)

    pylab.contourf(meshes[0], meshes[1], values, cmap=pylab.cm.PRGn)

    pylab.xlim(meshes[0][0], meshes[0][-1])
    pylab.ylim(meshes[1][0], meshes[1][-1])
