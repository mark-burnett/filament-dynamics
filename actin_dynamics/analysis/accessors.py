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


def get_factin(run, initial_value=0):
    basic_length = run.get_measurement('length')
    if initial_value is not None:
        corrected_length = utils.add_number(basic_length,
                -basic_length[1][0] + initial_value)
    else:
        corrected_length = basic_length
    return utils.scale_measurement(corrected_length,
            run.get_parameter('filament_tip_concentration'))

def get_scaled(run, measurement_name,
               parameter_name='filament_tip_concentration'):
    basic = run.get_measurement(measurement_name)
    return utils.scale_measurement(basic, run.get_parameter(parameter_name))

def get_multilpe_scaled(run, measurement_names,
                        parameter_name='filament_tip_concentration'):
    results = []
    for name in measurement_names:
        results.append(get_scaled(run, name, parameter_name=parameter_name))
    return utils.add_measurements(results)
