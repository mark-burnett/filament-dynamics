#    Copyright (C) 2011 Mark Burnett
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


def collate_on_times(flat_data):
    times = get_times(flat_data)
    values = []
    for t in times:
        values.append(get_values_at_time(flat_data, t))
    return times, values

def collate_on_indices(flat_values):
    values = []
    for i in xrange(len(times)):
        local_values = []
        values.append(local_values)
        for d in flat_values:
            if i < len(d):
                local_values.append(d[i])

    return values


def get_times(flat_data):
    smallest_time, largest_time, sample_period = get_time_bounds(flat_data)
    return list(numpy.arange(smallest_time,
        largest_time + sample_period/2, sample_period))

def get_time_bounds(flat_data):
    smallest_time = None
    largest_time = None
    sample_period = None
    for times, values in flat_data:
        if smallest_time is None:
            smallest_time = times[0]
            largest_time = times[-1]
            sample_period = float(times[1] - times[0])
        elif smallest_time > times[0]:
            smallest_time = times[0]
        elif largest_time < times[-1]:
            largest_time = times[-1]
    return smallest_time, largest_time, sample_period


def get_values_at_time(flat_data, time):
    results = []
    for times, values in flat_data:
        index = bisect.bisect_left(times, time)
        try:
            results.append(values[index])
        except IndexError:
            pass
    return results
