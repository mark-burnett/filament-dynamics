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

import numpy

__all__ = ['filename', 'perform', 'csv', 'plot']

filename = 'length_timecourses'

def perform(data, sample_period=0.5, **kwargs):
    raw_times       = [d['simulation_time'] for d in data]
    raw_lengths     = [d['strand_length'] for d in data]
    max_time        = max(t[-1] for t in raw_times)

    sample_times    = numpy.arange(0, max_time, sample_period)
    sampled_lengths = [numpy.interp(sample_times, t, d)
                        for t, d in itertools.izip(raw_times, raw_lengths)]

    return sample_times, sampled_lengths

def csv(results, **kwargs):
    times, lengths = results
    return itertools.izip(times, *lengths)

def plot(results, **kwargs):
    import pylab # Don't waste time importing for plain CSV dump
    pass
