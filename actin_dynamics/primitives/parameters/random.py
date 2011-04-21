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

import numpy

class Distribution(Parameter):
    skip_registration = True
    def __init__(self, **kwargs):
        Parameter.__init__(self, **kwargs)

    def __iter__(self):
        return self

    def next(self):
        return self.function()


class NormalDistribution(Distribution):
    '''
    Simple Gaussian distribution.
    Two tailed.
    '''
    def __init__(self, mean=None, standard_deviation=None, **kwargs):
        mean = float(mean)
        standard_deviation = float(standard_deviation)

        self.function = numpy.random.normal(loc=mean, scale=standard_deviation)

        Distribution.__init__(self, **kwargs)

    def allowed_value(self, value):
        return True


class GammaDistribution(Distribution):
    '''
    Gamma distribution has one tail at Inf, and is limited to 0.
    '''
    def __init__(self, mean=None, standard_deviation=None, **kwargs):
        mean = float(mean)
        standard_deviation = float(standard_deviation)

        k = (mean / standard_deviation)**2
        theta = mean / k

        self.function = numpy.random.gamma(shape=k, scale=theta)

        Distribution.__init__(self, **kwargs)

    def allowed_value(self, value):
        return value >= 0


class BetaDistribution(Distribution):
    '''
    Beta distribution has no tails.
    Specify lower_limit and upper_limit to control the bounds.
    '''
    def __init__(self, mean=None, standard_deviation=None,
                 lower_limit=0, upper_limit=1, **kwargs):
        self.lower_limit = float(lower_limit)
        self.upper_limit = float(upper_limit)
        mean = float(mean)
        standard_deviation = float(standard_deviation)

        beta = mean * (1 - mean)**2 / standard_deviation**2 + mean - 1
        alpha = beta * mean / (1 - mean)

        width = self.upper_limit - self.lower_limit

        self.function = lambda: (
                width * numpy.random.beta(a=alpha, b=beta)
                + self.lower_limit)

        Distribution.__init__(self, **kwargs)

    def allowed_value(self, value):
        return self.lower_limit <= value <= self.upper_limit
