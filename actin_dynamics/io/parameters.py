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

import itertools

import yaml
import numpy

class ParameterMeshIterator(object):
    def __init__(self, names, parameter_sets):
        self.names = names
        self.parameter_sets = parameter_sets
    
    def __iter__(self):
        return self

    def next(self):
        next_parameter_sets = next(self.parameter_sets)
        return dict((n, v) for n, v in itertools.izip(self.names,
                                                      next_parameter_sets))


def _make_mesh(min_value, max_value, mesh_size, mesh_type):
    if 'linear' == mesh_type.lower():
        return numpy.linspace(min_value, max_value, mesh_size)
    elif 'log' == mesh_type.lower():
        umin_value = numpy.log(min_value)
        umax_value = numpy.log(max_value)
        transformed_range = numpy.linspace(umin_value, umax_value, mesh_size)
        return numpy.exp(transformed_range)
    else:
        raise RuntimeError('Unsupported mesh type specified for make_mesh.')

def _make_parameter_mesh_iterator(parameter_ranges):
    names = []
    meshes = []
    for name, range_info in parameter_ranges.iteritems():
        names.append(name)
        meshes.append(_make_mesh(*range_info))

    parameter_sets = itertools.product(*meshes)
    
    return ParameterMeshIterator(names, parameter_sets)

def parse_parameters_file(par_file):
    parameter_ranges = yaml.load(par_file)
    return _make_parameter_mesh_iterator(parameter_ranges)
