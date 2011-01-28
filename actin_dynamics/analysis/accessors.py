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

from . import utils

def get(parameter_set, name):
    return parameter_set['sem'][name]

def get_length(parameter_set):
    basic_length = parameter_set['sem']['length']
    subtracted_length = utils.add_number(basic_length,
            -basic_length[1][0])
    return utils.scale_measurement(subtracted_length,
            parameter_set['parameters']['filament_tip_concentration'])

def get_scaled(parameter_set, name):
    basic = parameter_set['sem'][name]
    return utils.scale_measurement(basic,
            parameter_set['parameters']['filament_tip_concentration'])
