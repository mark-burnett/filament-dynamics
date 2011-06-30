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
import math

import numpy

def collection_stats(value_collection):
    all_vals = numpy.fromiter(itertools.chain(*value_collection), dtype=float)
    mean = numpy.mean(all_vals)
    std = numpy.std(all_vals)
    return mean, std



def aggregate_autocorrelation(sample_period, value_collection):
    big_mean, big_std = collection_stats(value_collection)

    correlation_collection = [
            autocorrelation(values, mean=big_mean, std=big_std)
            for values in value_collection]

    maxlen = max(map(len, correlation_collection))
    collated_correlations = []
    for i in xrange(maxlen):
        local_correlations = []
        collated_correlations.append(local_correlations)
        for correlations in correlation_collection:
            if i < len(correlations):
                local_correlations.append(correlations[i])

    taus = numpy.arange(maxlen) * sample_period
    means = [numpy.mean(acs) for acs in collated_correlations]

    return taus, means, [0 for t in taus]


def autocorrelation(values, mean=None, std=None):
    '''
    Perform a proper statistical autocorrelation.
    '''
    values = numpy.array(values, dtype=float)

    if not mean:
        mean = numpy.mean(values)
    if not std:
        std = numpy.std(values)

    values = values - mean

    length = len(values)
    result = [sum(values**2)/length]
    for i in xrange(1, len(values)):
        result.append((values[i:]*values[:-i]).sum()/(length - i))
    return numpy.array(result) / std**2
