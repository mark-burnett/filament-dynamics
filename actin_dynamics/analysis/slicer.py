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

import bisect
import collections
import itertools

import numpy

class Slicer(object):
    def __init__(self, axis_values, lookup, parameter_sets):
        self.axis_values = axis_values
        self.lookup = lookup
        self.parameter_sets = parameter_sets

    @classmethod
    def from_parameter_sets(cls, parameter_sets, parameter_names):
        # Collect parameter values
        parameter_values = collections.defaultdict(set)
        for ps in parameter_sets:
            for name in parameter_names:
                parameter_values[name].add(ps['parameters'][name])

        # Arrange parameter values in list
        axis_values = []
        for name in parameter_names:
            axis_values.append(sorted(parameter_values[name]))

        # Fill in lookup values
        lookup = -numpy.ones([len(av) for av in axis_values], dtype=int)
        for ps_index, ps in enumerate(parameter_sets):
            coords = tuple([bisect.bisect_left(av, ps['parameters'][name])
                            for av, name in itertools.izip(axis_values,
                                                           parameter_names)])
            lookup[coords] = ps_index

        return cls(axis_values, lookup, parameter_sets)


    def __getitem__(self, par_values):
        return self.parameter_sets[self.lookup[self._get_coords(par_values)]]


    def _get_coords(self, par_values):
        coords = []
        for pv, av in itertools.izip(par_values, self.axis_values):
#            if type(pv) is slice:
#                coords.append(pv)
#            else:
                coords.append(bisect.bisect_left(av, pv))
        return tuple(coords)

class NestingSlicer(object):
    @classmethod
    def from_stuff(cls, parameter_sets, parameter_names, atp_weights,
                   method=None):
        pass
