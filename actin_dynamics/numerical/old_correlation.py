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

#import itertools
#import math
#
#import numpy
#
#def collection_stats(value_collection):
#    all_vals = list(itertools.chain(*value_collection))
#    mean = numpy.mean(all_vals)
#    std = numpy.std(all_vals)
#    return mean, std
#
## NOTE weighted_avg_and_std taken from EOL on StackOverflow
## http://stackoverflow.com/questions/2413522/weighted-std-in-numpy
#def weighted_avg_and_std(values, weights):
#    """
#    Returns the weighted average and standard deviation.
#
#    values, weights -- Numpy ndarrays with the same shape.
#    """
#    average = numpy.average(values, weights=weights)
#    variance = numpy.dot(weights, (values-average)**2)/weights.sum()  # Fast and numerically precise
#    return (average, math.sqrt(variance))
#
#
#def get_values_at_time(flat_data, time):
#    results = []
#    for times, values in flat_data:
#        index = bisect.bisect_left(times, time)
#        try:
#            results.append(values[index])
#        except IndexError:
#            pass
#    return results
#
#def aggregate_autocorrelation(sample_period, value_collection):
#    big_sum = 0
#    big_count = 0
#    for single_values in value_collection:
#        big_sum += sum(single_values)
#        big_count += len(single_values)
#    big_mean = float(big_sum) / big_count
#    print 'BM', big_mean
#
#    correlations = []
#    counts = []
#    for single_values in value_collection:
#        ac_values, ac_counts = autocorrelate(single_values, mean=big_mean)
#        correlations.append(ac_values)
#        counts.append(ac_counts)
#
#    maxlen = max(map(len, correlations))
#    collated_acs = []
#    collated_counts = []
#    for i in xrange(maxlen):
#        local_acs = []
#        local_counts = []
#        collated_acs.append(local_acs)
#        collated_counts.append(local_counts)
#        for acs, cts in itertools.izip(correlations, counts):
#            if i < len(acs):
#                local_acs.append(acs[i])
#                local_counts.append(cts[i])
#
#    taus = numpy.arange(maxlen) * sample_period
#    ac_means = []
#    ac_errors = []
#    for acs, cts in itertools.izip(collated_acs, collated_counts):
#        acs = numpy.array(acs)
#        cts = numpy.array(cts)
#        mean, std = weighted_avg_and_std(acs, cts)
#        ctssum = float(cts.sum())
#        # XXX This error is not representitive for small samples.
#        error = std / math.sqrt(ctssum)
##        if ctssum > 1:
##            error = std / math.sqrt(ctssum)
##        else:
##            error = mean
#        ac_means.append(mean)
#        ac_errors.append(error)
#
#    return taus, ac_means, ac_errors
#
#def autocorrelate(values, mean=1):
#    values = numpy.array(values)
#    result, count = correlate(values, values, mean=mean)
#    results = [result]
#    counts = [count]
#    for i in xrange(1, len(values)):
#        result, count = correlate(values[i:], values[:-i], mean=mean)
#        results.append(result)
#        counts.append(count)
#    return results, counts
#
#def correlate(a, b, mean=1):
#    length = len(a)
#    return sum(a * b) / mean / float(length), length

import itertools

import numpy

def collection_stats(value_collection):
    all_vals = numpy.fromiter(itertools.chain(*value_collection), dtype='double')
    mean = numpy.mean(all_vals)
    std = numpy.std(all_vals)
    return mean, std


def aggregate_autocorrelation(sample_period, value_collection):
    big_mean, big_std = collection_stats(value_collection)

    correlation_collection = [autocorrelate(values, normalization=big_mean)
            for values in value_collection]

    maxlen = max(map(len, correlation_collection))
    collated_correlations = []
    for i in xrange(maxlen):
        local_correlations = []
        collated_correlations.append(local_correlations)
        for correlations in correlation_collection:
            if i < len(acs):
                local_correlations.append(correlations[i])

    taus = numpy.arange(maxlen) * sample_period
    means = [numpy.mean(acs) for acs in collated_correlations]

    return taus, means, [0 for t in taus]

def autocorrelate(values, normalization=1):
    length = len(values)
    values = numpy.array(values, dtype='double')
    return numpy.correlate(values, values, mode='same')[length/2:] / (
            length * normalization)
