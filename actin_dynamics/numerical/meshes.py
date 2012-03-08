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

import numpy

class ParameterMeshIterator(object):
    def __init__(self, names, parameter_sets):
        self.names = names
        self.parameter_sets = itertools.product(*parameter_sets)
    
    def __iter__(self):
        return self

    def next(self):
        next_parameter_sets = self.parameter_sets.next()
        if next_parameter_sets:
            return dict((n, v) for n, v in itertools.izip(self.names,
                                                          next_parameter_sets))
        else:
            raise StopIteration()

def make_mesh(lower_bound, upper_bound, num_points, mesh_type):
    '''
    Mesh includes the upper bound:  [lower_bound, upper_bound]
    '''
    if 'linear' == mesh_type.lower():
        return numpy.linspace(lower_bound, upper_bound, num_points)
    elif 'log' == mesh_type.lower():
        return log_mesh(lower_bound, upper_bound, num_points)
    elif 'shiftlog' == mesh_type.lower():
        return shiftlog_mesh(lower_bound, upper_bound, num_points)
    elif 'splitlog' == mesh_type.lower():
        return splitlog_mesh(lower_bound, upper_bound, num_points)
    elif 'tan' == mesh_type.lower():
        return tan_mesh(lower_bound, upper_bound, num_points)
    elif 'split' == mesh_type.lower():
        return split_mesh(lower_bound, upper_bound, num_points)
    else:
        raise RuntimeError('Unsupported mesh type specified for make_mesh.')

def log_mesh(lower_bound, upper_bound, num_points):
    ulower_bound = math.log(lower_bound)
    uupper_bound = math.log(upper_bound)
    transformed_range = numpy.linspace(ulower_bound, uupper_bound,
                                           num_points)
    return numpy.exp(transformed_range)

def shiftlog_mesh(lower_bound, upper_bound, num_points):
    '''
    Make a mesh that's part log, part linear, and includes exact end points.
    '''
    # scale UB -> 1.5, LB=0 -> 0.5
    llb = numpy.log(0.5)
    lub = numpy.log(1.5)

    linmesh = numpy.linspace(llb, lub, num_points)
    logmesh = numpy.exp(linmesh)
    logmesh -= 0.5 - lower_bound
    logmesh *= upper_bound

    return logmesh

def splitlog_mesh(lower_bound, upper_bound, num_points):
    split_point = float(upper_bound - lower_bound) / 2 + lower_bound

    lower_mesh = log_mesh(lower_bound, split_point, num_points / 2 + 1)
    upper_mesh = numpy.linspace(split_point, upper_bound, num_points / 2 + 1)

    return numpy.hstack((lower_mesh[:-1], upper_mesh))

def split_mesh(lower_bound, upper_bound, num_points):
    split_point = float(upper_bound - lower_bound) / 5 + lower_bound

    lower_mesh = numpy.linspace(lower_bound, split_point, num_points / 2 + 1)
    upper_mesh = numpy.linspace(split_point, upper_bound, num_points / 2 + 1)

    return numpy.hstack((lower_mesh[:-1], upper_mesh))

def tan_mesh(lower_bound, upper_bound, num_points):
    tlb = numpy.arctan(lower_bound)
    tub = numpy.arctan(upper_bound)

    transformed_mesh = numpy.linspace(tlb, tub, num_points)
    return numpy.tan(transformed_mesh)


def parameters_from_spec(par_specs):
    names = []
    values = []
    for name, kwargs in par_specs.iteritems():
        names.append(name)
        values.append(make_mesh(**kwargs))

    return ParameterMeshIterator(names, values)
