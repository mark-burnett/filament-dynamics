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
        ulower_bound = math.log(lower_bound)
        uupper_bound = math.log(upper_bound)
        transformed_range = numpy.linspace(ulower_bound, uupper_bound,
                                               num_points)
        return [math.exp(tr) for tr in transformed_range]
    elif 'shiftlog' == mesh_type.lower():
        return shiftlog_mesh(lower_bound, upper_bound, num_points)
    else:
        raise RuntimeError('Unsupported mesh type specified for make_mesh.')

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


def parameters_from_spec(par_specs):
    names = []
    values = []
    for name, kwargs in par_specs.iteritems():
        names.append(name)
        values.append(make_mesh(**kwargs))

    return ParameterMeshIterator(names, values)
