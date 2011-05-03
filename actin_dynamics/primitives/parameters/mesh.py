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

from .base_classes import Parameter

def mesh_generator(lower_bound, upper_bound, step_size, error=1e-3):
    epsilon = error * step_size
    value = lower_bound
    while value <= upper_bound + epsilon:
        yield value
        value += step_size

class Mesh(Parameter):
    def __init__(self, lower_bound=None, upper_bound=None,
                 num_points=None, step_size=None, **kwargs):
        self.lower_bound = float(lower_bound)
        self.upper_bound = float(upper_bound)
        if num_points:
            self.step_size = (self.upper_bound - self.lower_bound) / (
                    num_points - 1)
        else:
            self.step_size = float(step_size)

        Parameter.__init__(self, **kwargs)

    def __iter__(self):
        return mesh_generator(self.lower_bound, self.upper_bound,
                              self.step_size)
