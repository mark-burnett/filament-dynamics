#!/usr/bin/env python
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
import bisect

import numpy

import tools
from simple import csv

__all__ = ['filename', 'perform', 'csv', 'plot']

filename = 'mitchison_stability'

def perform(data, sample_period=1,
            stable_time=100, stable_variation=100,
            **kwargs):
    # Raw data
    raw_times   = [d['simulation_time'] for d in data]
    raw_lengths = [d['strand_length'] for d in data]
    max_time   = max(t[-1] for t in raw_times)

    # Sample the data using sample period.
    sample_times    = numpy.arange(0, max_time, sample_period)
    sampled_lengths = map(lambda t, d: numpy.interp(sample_times, t, d, -1),
                          raw_times, raw_lengths)

    stable_samples  = int(stable_time/sample_period)

    # Cut off values past depolymerization point.
    cut_lengths = []
    for sl in sampled_lengths:
        index = len(sl)
        for i, v in enumerate(sl):
            if v <= 1:
                index = i
                break
        # Discard unusable rate profiles (eg those that are not long enough).
        if index > stable_samples:
            cut_lengths.append(sl[:index])

    # Calculate (poly/depoly) rates at each point.
    rate_profiles   = [(cl - numpy.roll(cl, stable_samples))
                       for cl in cut_lengths]

    # Check stability critereon at each point.
    stable_profiles = [numpy.abs(rp) < stable_variation for rp in rate_profiles]

    # Determine the fraction that is stable at each timestep, throwing away
    # filemants that have completely depolymerized.
    stable_histograms = tools.make_timecourse_histogram(stable_profiles)
    stable_fractions  = [float(sum(sh))/len(sh) for sh in stable_histograms]

    # Throw away left over chaff (from numpy.roll).
    return sample_times[:-stable_samples], stable_fractions[stable_samples:]

def plot():
    raise NotImplementedError()
    import pylab # Don't waste time importing for plain CSV dump
    pass
