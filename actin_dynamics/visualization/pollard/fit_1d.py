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

from .. import themes
from .. import slicing
from .. import measurements

def adppi(slicer, abscissa_name, theme=None):

    best_val, all_names, best_x = slicer.minimum_values()

    fixed_point = dict((n, x) for n, x in itertools.izip(all_names, best_x)
                       if n != abscissa_name)

    min_y, junk_name, min_x = slicer.minimum_values(abscissa_name)
    sl_y, junk_name, sl_x = slicer.slice(**fixed_point)

    if not theme:
        theme = themes.Variation(xlabel=abscissa_name)

    theme.initialize()

    measurements.plot_smooth((min_x[0], min_y), **theme())
    measurements.plot_smooth((sl_x[0], sl_y), **theme())
    
    theme.finalize()
