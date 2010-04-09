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

import bisect
import numpy

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

def histogram_stats(histograms):
    averages = map(numpy.average, histograms)
    stds = map(numpy.std, histograms)
    return averages, stds