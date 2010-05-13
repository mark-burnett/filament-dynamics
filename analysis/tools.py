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

def downsample(sample_times, data, extrapolate=False):
    x, y = zip(*data)

    if not extrapolate:
        true_sample_times = [t for t in sample_times if x[0] <= t <= x[-1]]
    else:
        true_sample_times = sample_times

    return numpy.interp(true_sample_times, x, y)

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
