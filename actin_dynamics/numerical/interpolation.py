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

def interp1d(x_data, y_data):
    def inner(x):
        left = bisect.bisect_left(x_data, x)
        if left > 0:
            result = linear_project(x_data[left - 1], y_data[left - 1],
                                    x_data[left],    y_data[left],
                                    x)
            return result
        else:
            raise IndexError

    return inner

def linear_resample(data, new_x):
    x_data, y_data = data

    if 1 == len(x_data):
        return new_x, [y_data[0] for x in new_x]

    linterp = interp1d(x_data, y_data)

    result = []
    for x in new_x:
        try:
            y = linterp(x)
        except IndexError:
            if x <= x_data[0]:
                y = linear_project(x_data[0], y_data[0],
                                   x_data[1], y_data[1], x)
            elif x > x_data[-1]:
                y = linear_project(x_data[-2], y_data[-2],
                                   x_data[-1], y_data[-1], x)
        result.append(float(y))

    return new_x, result

def linear_project(x1, y1, x2, y2, x3):
    m = (y2 - y1) / (x2 - x1)
    return y1 + m * (x3 - x1)

def previous_value_resample(data, new_x):
    x_data, y_data = data

    low_x = 0

    results = []
    for x in new_x:
        left_xi  = bisect.bisect_left(x_data, x, lo=low_x)
        right_xi = bisect.bisect_right(x_data, x, lo=low_x)
        xi = max(left_xi, right_xi) - 1
        results.append(y_data[xi])
        low_x = xi

    return new_x, results


# Interpolation methods should be registered here for convenience.
interpolation_methods = {'linear': linear_resample,
                         'previous_value': previous_value_resample}


def resample_measurement(measurement, sample_times, method='linear'):
    if str == type(method):
        resample = interpolation_methods[method]
    else:
        resample = method

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
