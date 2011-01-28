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
import math

import yaml

# XXX This is an itertools work-alike.  It is needed because it was
#     introduced in python 2.6, but pypy is stuck at 2.5 as of now.
def _product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def _linspace(min_value, max_value, num_points):
    if num_points > 1:
        dx = float(max_value - min_value) / (num_points - 1)
        return [min_value + i * dx for i in xrange(num_points)]
    else:
        return [min_value]

class ParameterMeshIterator(object):
    def __init__(self, names, parameter_sets):
        self.names = names
        self.parameter_sets = parameter_sets
    
    def __iter__(self):
        return self

    def next(self):
        next_parameter_sets = self.parameter_sets.next()
        return dict((n, v) for n, v in itertools.izip(self.names,
                                                      next_parameter_sets))


def _make_mesh(min_value, max_value, mesh_size, mesh_type):
    if 'linear' == mesh_type.lower():
        return _linspace(min_value, max_value, mesh_size)
    elif 'log' == mesh_type.lower():
        umin_value = math.log(min_value)
        umax_value = math.log(max_value)
        transformed_range = _linspace(umin_value, umax_value, mesh_size)
        return [math.exp(tr) for tr in transformed_range]
    else:
        raise RuntimeError('Unsupported mesh type specified for make_mesh.')

def _make_split_mesh(process_number, num_processes, *range_info):
    full_mesh = _make_mesh(*range_info)

    size = len(full_mesh)
    fraction = 1.0 / num_processes
    width = int(size * fraction) # Round down.

    # Be sure to get the extra couple of points on the end.
    if process_number == num_processes:
        return full_mesh[(process_number - 1) * width:]

    return full_mesh[(process_number - 1) * width:process_number * width]


def _make_parameter_mesh_iterator(parameter_ranges, split_parameter_name,
                                  process_number, num_processes):
    names = []
    meshes = []
    for name, range_info in parameter_ranges.iteritems():
        names.append(name)
        if split_parameter_name and name == split_parameter_name:
            meshes.append(_make_split_mesh(process_number, num_processes,
                                           *range_info))
        else:
            meshes.append(_make_mesh(*range_info))
    
    return ParameterMeshIterator(names, _product(*meshes))


def parse_parameters_file(par_file, split_parameter_name=None,
                          process_number=0, num_processes=1):
    parameter_ranges = yaml.load(par_file)
    return _make_parameter_mesh_iterator(parameter_ranges,
                                         split_parameter_name,
                                         process_number, num_processes)
