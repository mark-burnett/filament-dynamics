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

import numpy

from . import sampling

def avg_std(times, data):
    averages = []
    stds = []
    for di in data:
        averages.append(numpy.average(di))
        stds.append(numpy.std(di))

    return averages, stds

def statistical_analysis(sim_data, property_name, duration, sample_period):
    property_data = [d[property_name] for d in sim_data]
    sample_times = numpy.arange(0, duration, float(sample_period))

    sampled_property_data = sampling.downsample_each(sample_times,
                                                     property_data)

    return sample_times, avg_std(sample_times, sampled_property_data)
