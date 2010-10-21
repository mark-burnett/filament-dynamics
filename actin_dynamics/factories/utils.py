#    Copyright (C) 2010 Mark Burnett
# #    This program is free software: you can redistribute it and/or modify
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
