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

class ParameterConstraint(object):
    def __init__(self, lower_bound=None, upper_bound=None,
                 mean=None, standard_deviation=None,
                 allowed_values=None, distribution=None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.mean = mean
        self.standard_deviation = standard_deviation

        self.allowed_values = allowed_values

        if distribution:
            self.distribution = distribution
        else:
            distribution = 'flat'

    @property
    def width(self):
        if standard_deviation:
            return standard_deviation
        else:
            return self.upper_bound - self.lower_bound


def fixed(value):
    return ParameterConstraint(lower_bound=value, upper_bound=value)

def range(lower_bound, upper_bound, distribution=None):
    return ParameterConstraint(lower_bound=lower_bound, upper_bound=upper_bound,
                               distribution=distribution)

def fixed_values(values, distribution=None):
    return ParameterConstraint(allowed_values=values,
                               lower_bound=min(allowed_values),
                               upper_bound=max(allowed_values),
                               distribution=distribution)
