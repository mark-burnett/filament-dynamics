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

from simple import csv

__all__ = ['filename', 'perform', 'csv', 'plot']

filename = 'cleavage_integral'

def perform(data, sample_period=1, **kwargs):
    raw_times    = [d['simulation_time'] for d in data]
    raw_cleavage = [d['cleavage_events'] for d in data]
    max_time     = max(t[-1] for t in raw_times)

    sample_times     = numpy.arange(0, max_time, sample_period)
    sampled_cleavage = [numpy.interp(sample_times, t, d)
                        for t, d in itertools.izip(raw_times, raw_cleavage)]

    return sample_times, map(numpy.average, itertools.izip(*sampled_cleavage))

def plot(results, **kwargs):
    import pylab # Don't waste time importing for plain CSV dump
    pass
