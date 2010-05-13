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

from . import tools

def make_csv(data, sample_period=-1.0, duration=-1.0,
             filament_tip_concentration=None,
             seed_length=None, seed_concentration=None,
             **kwargs):
    sample_period = float(sample_period)
    sample_times  = numpy.arange(0, duration, sample_period)

    length_data = [d['length'] for d in data]

    sampled_lengths = zip(*[tools.downsample(sample_times, ld, extrapolate=True)
                            for ld in length_data])
    averages = numpy.array([numpy.average(sl) for sl in sampled_lengths])

    if seed_length:
        averages -= float(seed_length)

    if filament_tip_concentration:
        averages *= float(filament_tip_concentration)
        if seed_concentration:
            averages -= float(seed_concentration)


    return itertools.izip(sample_times, averages)
