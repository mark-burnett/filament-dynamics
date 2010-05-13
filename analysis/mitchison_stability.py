#!/usr/bin/env python
#    Copyright (C) 2010 Mark Burnett #
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
import csv

import numpy

from . import tools

def make_csv(data, sample_period=-1.0, duration=-1.0,
             stable_time=100, stable_rate=1,
             data_file=None,
             **kwargs):
    """
    sample_period = None -> use data file for time points
    duration = None -> only needed if sample_period != None
    """
    stable_time = float(stable_time)
    if sample_period > 0:
        sample_times = numpy.arange(stable_time + 1, duration, float(sample_period))
    elif data_file:
        # Read in data from file.
        r = csv.reader(data_file, delimiter=' ')
        sample_times = []
        for row in r:
            try:
                value = float(row[0])
            except:
                value = float(row[1])
            sample_times.append(value)
        sample_times = numpy.array(sample_times)
    else:
        raise RuntimeError(
                'Must have either sample period or data file to generate csv.')

    original_lengths = [d['length'] for d in data]
    original_samples = [tools.downsample(sample_times, ol) for ol in original_lengths]
    old_samples      = [tools.downsample(sample_times - stable_time, ol)
                        for ol in original_lengths]
    sampled_rates    = [(orig - old[:len(orig)]) / stable_time
                        for orig, old in itertools.izip(original_samples,
                                                        old_samples)]
    timecourse_rates = tools.make_timecourse_histogram(sampled_rates)

    stable_count = [list(numpy.abs(r) < stable_rate).count(True)
                    for r in timecourse_rates]
    total_count  = [len(r) for r in timecourse_rates]
    stable_frac  = [float(sc) / tc
                    for sc, tc in itertools.izip(stable_count, total_count)]
    stat_errors  = [frac / numpy.sqrt(tc)
                    for frac, tc in itertools.izip(stable_frac, total_count)]

    return itertools.izip(sample_times, stable_frac, stat_errors)
