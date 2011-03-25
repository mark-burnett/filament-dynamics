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

from . import workalike

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
    effective_ub = (upper_bound - lower_bound) / (2 * num_points) + upper_bound

    if 'linear' == mesh_type.lower():
        return workalike.linspace(lower_bound, effective_ub, num_points)
    elif 'log' == mesh_type.lower():
        ulower_bound = math.log(lower_bound)
        uupper_bound = math.log(effective_ub)
        transformed_range = workalike.linspace(ulower_bound, uupper_bound,
                                               num_points)
        return [math.exp(tr) for tr in transformed_range]
    else:
        raise RuntimeError('Unsupported mesh type specified for make_mesh.')


def parameters_from_spec(par_specs):
    names = []
    values = []
    for name, kwargs in par_specs.iteritems():
        names.append(name)
        values.append(make_mesh(**kwargs))

    return ParameterMeshIterator(names, values)
