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

import numpy

from . import tools

def make_csv(data, sample_period=None, duration=-1.0, filament_tip_concentration=None, **kwargs):
    if sample_period is None:
        raise ValueError('sample_period not specified.')
    sample_period = float(sample_period)
    assert sample_period > 0

    filament_tip_concentration = float(filament_tip_concentration)

    sample_times = numpy.arange(0, duration, sample_period)
    release_data = [d['phosphate_release'] for d in data]
    sampled_data  = zip(*[tools.downsample(sample_times, rd, extrapolate=True)
                          for rd in release_data])
    averages = [numpy.average(sd) for sd in sampled_data]

    return itertools.izip(sample_times, averages)
