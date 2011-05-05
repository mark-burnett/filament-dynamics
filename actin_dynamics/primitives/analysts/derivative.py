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

import numpy

from .base_classes import Analyst
from . import analyst_utils

from actin_dynamics import database
from actin_dynamics.numerical import transform

class KeyedDerivative(Analyst):
    def __init__(self, source_name=None, source_type=None, *args, **kwargs):
        self.source_name = source_name
        self.source_type = source_type

        Analyst.__init__(self, *args, **kwargs)

    def analyze(self, observations, analyses):
        source = analyst_utils.choose_source(observations, analyses,
                self.source_type)
        keyed_data = transform.key_transform(source[self.source_name])
        results = {}
        for name, raw_data in keyed_data.iteritems():
            times, values = raw_data[0] # There should be only one element.
            sample_period = float(times[1] - times[0])
            values = numpy.array(values)
            d = numpy.diff(values) / sample_period
            results[name] = times[:-1], list(d)

        return database.Analysis(value=results)
