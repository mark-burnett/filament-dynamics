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

class ParameterMeshIterator(object):
    def __init__(self, names, values):
        self.names = names
        self.values = values
    
    def __iter__(self):
        return self

    def next(self):
        next_values = next(self.values)
        return dict((n, v) for n, v in itertools.izip(self.names, next_values))

def make_parameter_mesh_iterator(parameter_ranges):
    names = []
    values = []
    for name, range_info in parameter_ranges.iteritems():
        pass
    return ParameterMeshIterator(names, values)
