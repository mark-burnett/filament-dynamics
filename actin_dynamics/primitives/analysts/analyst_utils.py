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
import math

from actin_dynamics.numerical import workalike


def flatten_data(raw_data):
    flat_data = []
    for rd in raw_data:
        if isinstance(rd, dict):
            flat_data.extend(rd.itervalues())
        else:
            flat_data.append(rd)
    return flat_data


def collate_data(raw_data):
    flat_data = flatten_data(raw_data)
    times = get_times(flat_data)
    values = []
    for t in times:
        values.append(get_values_at_time(flat_data, t))
    return times, values


def get_times(flat_data):
    smallest_time, largest_time, sample_period = get_time_bounds(flat_data)
    return workalike.arange(smallest_time, largest_time + float(sample_period)/2,
            sample_period)

def get_time_bounds(flat_data):
    smallest_time = None
    largest_time = None
    sample_period = None
    for times, values in flat_data:
        if smallest_time is None:
            smallest_time = times[0]
            largest_time = times[-1]
            sample_period = times[1] - times[0]
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


def standard_error_of_mean(collated_data, scale_by=1, add=0):
    means = []
    errors = []
    for values in collated_data:
        length = len(values)
        sqrt_N = math.sqrt(length)

        adjusted_values = [float(v) * scale_by for v in values]
        mean = sum(adjusted_values) / length
        error = workalike.std(adjusted_values, mean) / sqrt_N
        means.append(mean + add)
        errors.append(error)
    return means, errors

def choose_source(observations, analyses, source_type):
    if 'observation' == source_type.lower():
        source = observations
    elif 'analyses' == source_type.lower():
        source = analyses
    else:
        raise RuntimeError('Unknown source type %r.' % source_type)
    return source
