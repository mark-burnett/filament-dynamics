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

import scipy

def resample(data, sample_times):
    '''
    Downsample data to sample_times.

    Tries to use well behaved interpolation methods if there are
    enough points.  If not, it improvises.
    '''
    times, values = data

    if len(values) < 2:
        return sample_times, [values[0] for t in sample_times]
    elif len(values) < 4:
        interp = scipy.interpolate.interp1d(times, values, bounds_error=False,
                                            fill_value=values[-1])
        return sample_times, interp(sample_times)
    else:
        bbox = [min(sample_times[0], times[0]),
                max(sample_times[-1], times[-1])]
        interp = scipy.interpolate.InterpolatedUnivariateSpline(
                times, values, bbox=bbox)
        return sample_times, interp(sample_times)

def resample_measurement(measurement, sample_times):
    # Resample value
    value_data = measurement[:2]

    result = resample(value_data, sample_times)

    # Resample error
    if 3 == len(measurement):
        error_data = measurement[0], measurement[2]
        junk_times, sampled_error = resample(error_data, sample_times)
        result = list(result)
        result.append(sampled_error)

    return result
