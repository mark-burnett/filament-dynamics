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

__all__ = ['summarize', 'downsample', 'make_timecourse_histogram']

def summarize(data):
    """
    Return the average and standard deviation of each quantity.
    """
    try:
        time    = data['time']
        results = {u'time': time}
        for name, values in data.items():
            if 'time' == name:
                continue
            results[name] = (map(numpy.average, itertools.izip(*values)),
                             map(numpy.std,     itertools.izip(*values)))
        return results
    except KeyError:
        return {}

def downsample(data, sample_period, duration):
    """
    Sample the raw data using sample_period.
    """
    try:
        raw_time     = [d['simulation_time'] for d in data]
        sampled_time = numpy.arange(0, duration, sample_period)
        sampled_data = {u'time': sampled_time}

        for name in data[0].keys():
            if 'simulation_time' == name or 'final_strand' == name:
                continue
            sampled_data[name] = [numpy.interp(sampled_time, t, d[name])
                                  for t, d in itertools.izip(raw_time, data)]

        return sampled_data
    except KeyError:
        return {}

def make_timecourse_histogram(timecourses):
    max_len = max(map(len, timecourses))
    histograms = []
    for i in xrange(max_len):
        hg = []
        for tc in timecourses:
            try:
                hg.append(tc[i])
            except IndexError:
                pass
        histograms.append(hg)
    return histograms
