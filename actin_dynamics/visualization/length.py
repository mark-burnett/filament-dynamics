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

from actin_dynamics.io import hdf as _hdf

#from . import utils as _utils

def get_length(analysis=None, parameter_set_number=None, zero_initial=True):
    times, average_length, lower_bound, upper_bound = (
            _utils.get_measurement_summary(analysis, parameter_set_number,
                                           'length'))
    if zero_initial:
        initial_length = average_length[0]
        average_length = [al - initial_length for al in average_length]
        lower_bound    = [lb - initial_length for lb in lower_bound]
        upper_bound    = [ub - initial_length for ub in upper_bound]

    return times, average_length, lower_bound, upper_bound
