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

def make_many(f, parameter_value_map, db_items):
    items = []
    for dbi in db_items:
        item = f(parameter_value_map, dbi)
        items.append(item)

    return items

def make_parameter_value_map(parameter_set):
    parameter_map = {}
    for parameter in parameter_set.parameters:
        parameter_map[parameter.label] = parameter.value
    return parameter_map


import numpy

def make_mesh(min_value, max_value, mesh_size, mesh_type):
    if 'linear' == mesh_type.lower():
        return numpy.arange(min_value, max_value, mesh_size)
    elif 'log' == mesh_type.lower():
        umin_value = numpy.log(min_value)
        umax_value = numpy.log(max_value)
        transformed_range = numpy.arange(umin_value, umax_value, mesh_size)
        return numpy.exp(transformed_range)
    else:
        raise RuntimeError('Unsupported mesh type specified for make_mesh.')
