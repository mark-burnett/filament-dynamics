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


def collection_stats(value_collection):
    all_vals = numpy.fromiter(itertools.chain(*value_collection),
            dtype=float)
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

    return taus, means


def autocorrelation(values, mean=None, std=None):
    '''
    Perform a proper statistical autocorrelation.
    '''
    values, std = _groom_corr_values(values, mean=mean, std=std)

    result = [numpy.mean(values**2)]
    for i in xrange(1, len(values)):
        result.append(numpy.mean(values[i:]*values[:-i]))
    return numpy.array(result) / std**2


def correlation(a, b, a_mean=None, a_std=None, b_mean=None, b_std=None,
        full=True):
    '''
    Perform a proper statistical correlation.

    parameters:
        means & stds:  if none, these will be computed
        full:  if true, will return the full correlation, even with small overlap
    '''
    a, a_std = _groom_corr_values(a, mean=a_mean, std=a_std)
    b, b_std = _groom_corr_values(b, mean=b_mean, std=b_std)

    stdproduct = a_std * b_std

    a_length = len(a)
    b_length = len(b)

    # Make sure a is the longest sequence.
    if b_length > a_length:
        a, b = b, a
        a_length, b_length = b_length, a_length

    maxlength = a_length
    minlength = b_length

    # k_crit is the index at which we no longer have full overlap
    k_crit = maxlength - minlength + 1
    result = []
    # Fully overlapping portion
    for k in xrange(k_crit):
        aslice = a[k:k + minlength]
        bslice = b[:minlength]
        result.append(numpy.mean(aslice * bslice))

    if full:
        # Partially overlapping portion
        for k in xrange(k_crit, maxlength):
            overlap = minlength - (k - k_crit) - 1
            aslice = a[k:k + overlap]
            bslice = b[:overlap]
            result.append(numpy.mean(aslice * bslice))

    return numpy.array(result) / stdproduct


def _groom_corr_values(values, mean=None, std=None):
    '''
    Subtracts mean from values, and makes sure we're using the right std.
    '''
    values = numpy.array(values, dtype=float)
    if mean is None:
        mean = numpy.mean(values)
    if std is None:
        std = numpy.std(values)
    return values - mean, std
