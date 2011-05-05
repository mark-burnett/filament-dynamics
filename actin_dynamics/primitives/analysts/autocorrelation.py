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

import itertools

import numpy

from .base_classes import Analyst

from . import analyst_utils

from actin_dynamics import database
from actin_dynamics.numerical import measurements, utils

class Autocorrelation(Analyst):
    '''
    Calculates:
    c(tau) = <v(t0) * v(t0 + tau)> - <v>**2
    '''
    def __init__(self, source_name=None, source_type=None,
                 start_time=None, stop_time=None, *args, **kwargs):
        self.source_name = source_name
        self.source_type = source_type
        self.start_time = start_time
        self.stop_time = stop_time

        Analyst.__init__(self, *args, **kwargs)

    def analyze(self, observations, analyses):
        source = analyst_utils.choose_source(observations, analyses,
                self.source_type)
        data = source[self.source_name]
        (smallest_time, largest_time, sample_period
                ) = analyst_utils.get_time_bounds(data.itervalues())
        longest_sequence_length = _get_longest_sequence_length(
                data.itervalues())
        taus = numpy.arange(longest_sequence_length - 1) * sample_period
        correlation_values = [[] for tau in taus]
        stats = utils.RunningStats()
        for measurement in data.itervalues():
            times, values = measurements.time_slice(
                    measurement, self.start_time, self.stop_time)
            sample_period = times[1] - times[0]
            values = numpy.array(values)
            stats.append(values)
            for delta, cv in enumerate(correlation_values):
                ae = list(_autocorrelation_element(values, delta))
                cv.extend(ae)

        means, errors = analyst_utils.standard_error_of_mean(correlation_values)

        return database.Analysis(value=(taus, means, errors))

def _get_longest_sequence_length(measurements):
    longest = 0
    for times, values in measurements:
        if len(times) > longest:
            longest = len(times)
    return longest

def _autocorrelation_element(values, delta):
    if delta:
        for i, v in enumerate(values[:-delta]):
            yield v * values[i + delta]
    else:
        for v in values:
            yield v**2
