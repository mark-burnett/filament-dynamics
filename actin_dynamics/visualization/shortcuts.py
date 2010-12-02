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

from . import io as _io
from . import utils as _utils

from .length import get_length as _get_length
from .fluorescence import get_fluorescence as _get_fluorescence
from .fluorescence import normalize_fluorescence as _normalize_fluorescence

def write_length_vs_fluorescence(analysis=None, parameter_set_number=None,
                                 filename=None, filament_tip_concentration=None):
    length_measurement = _get_length(analysis, parameter_set_number)
    fluorescence_measurement = _get_fluorescence(analysis, parameter_set_number)

    normalized_fluorescence = _normalize_fluorescence(length_measurement,
                                                      fluorescence_measurement)

    scaled_length = _utils.scale_measurement(length_measurement,
                                             filament_tip_concentration)
    scaled_fluorescence = _utils.scale_measurement(normalized_fluorescence,
                                                   filament_tip_concentration)
    with open(filename, 'w') as f:
        _io.write_measurements(f, [scaled_length, scaled_fluorescence])
