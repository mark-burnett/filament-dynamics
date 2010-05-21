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

def make_csv(data, sample_period=-1.0, duration=-1.0, filament_tip_concentration=None, **kwargs):
    if filament_tip_concentration is None:
        raise RuntimeError('filament_tip_concentration required.')

    sample_period = float(sample_period)
    filament_tip_concentration = float(filament_tip_concentration)

    sample_times = numpy.arange(0, duration, sample_period)
    cleavage_data = [d['phosphate_cleavage'] for d in data]
    sampled_data  = zip(*[tools.downsample(sample_times, cd, extrapolate=True)
                          for cd in cleavage_data])
    averages = [numpy.average(sd) * filament_tip_concentration
                for sd in sampled_data]

    return itertools.izip(sample_times, averages)
