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

from . import base_classes

from actin_dynamics.numerical import interpolation
from actin_dynamics.numerical import measurements
from actin_dynamics.numerical import regression

from actin_dynamics import logger

log = logger.getLogger(__file__)


class HalfTime(base_classes.Objective):
    def __init__(self, analysis_name=None, base_value=None,
            subtract_fraction=0, second_subtract_fraction=0, *args, **kwargs):
        self.analysis_name = analysis_name
        self.half_value = float(base_value) * (
                1 - float(subtract_fraction)
                  - float(second_subtract_fraction)) / 2

        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        times, values, errors = run.analyses[self.analysis_name]

        target.value = _calc_halftime(times, values, self.half_value)

class HalfTimeError(base_classes.Objective):
    def __init__(self, analysis_name=None, base_value=None,
            subtract_fraction=0, second_subtract_fraction=0, *args, **kwargs):
        self.analysis_name = analysis_name
        self.half_value = float(base_value) * (
                1 - float(subtract_fraction)
                  - float(second_subtract_fraction)) / 2

        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        times, values, errors = run.analyses[self.analysis_name]
#        log.warn('times: %s', times)
#        log.warn('values: %s', values)
#        log.warn('errors: %s', errors)

        halftime = _calc_halftime(times, values, self.half_value)
#        log.warn('half_value = %s, calculated halftime = %s',
#                self.half_value, halftime)

        left_index = bisect.bisect_left(times, halftime)
        left_index = min(left_index, len(times) - 2)
#        log.warn('left_index = %s, times: %s', left_index,
#                times[left_index:left_index + 2])

        left_time, right_time = times[left_index:left_index + 2]
        left_value, right_value = values[left_index:left_index + 2]
        left_error, right_error = errors[left_index:left_index + 2]

        half_value_error = interpolation.linear_project(left_time, left_error,
                right_time, right_error, halftime)

        slope = (right_value - left_value) / (right_time - left_time)

        target.value = half_value_error / slope


# XXX This obviously breaks if the halftime isn't reached.
def _calc_halftime(times, values, half_value):
    for i, v in enumerate(values):
        if v > half_value:
            break;

    left_time = times[i-1]
    left_value = values[i-1]

    right_time = times[i]
    right_value = values[i]

    if (left_value == right_value):
        log.warn('Matching values: left = %s, right = %s', left_value, right_value)

    if (left_time == right_time):
        log.warn('Matching times: left = %s, right = %s', left_time, right_time)

    y = interpolation.linear_project(left_value, left_time,
            right_value, right_time, half_value)

    if y == float('nan'):
        log.error('Halftime is not a number: i = %s, lt = %s, rt = %s, lv = %s, rv = %s',
                i, left_time, right_time, left_value, right_value)
    return y

class PeakTime(base_classes.Objective):
    def __init__(self, analysis_name=None, *args, **kwargs):
        self.analysis_name = analysis_name
        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        times, values, errors = run.analyses[self.analysis_name]

        max_value = max(values)
        max_index = values.index(max_value)
        target.value = times[max_index]

class PeakValue(base_classes.Objective):
    def __init__(self, analysis_name=None, *args, **kwargs):
        self.analysis_name = analysis_name
        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        times, values, errors = run.analyses[self.analysis_name]

        max_value = max(values)
        target.value = max_value


class FitTau(base_classes.Objective):
    def __init__(self, analysis_name=None, start_time=None, *args, **kwargs):
        self.analysis_name = analysis_name
        self.start_time = float(start_time)

        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        times, values, errors = run.analyses[self.analysis_name]
        sliced_times, sliced_values = measurements.time_slice((times, values),
                start_time=self.start_time)
        tau, scale = regression.fit_exponential(sliced_times, sliced_values)
        target.value = tau

class FitMagnitude(base_classes.Objective):
    def __init__(self, analysis_name=None, start_time=None, *args, **kwargs):
        self.analysis_name = analysis_name
        self.start_time = float(start_time)

        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        times, values, errors = run.analyses[self.analysis_name]
        sliced_times, sliced_values = measurements.time_slice((times, values),
                start_time=self.start_time)
        tau, scale = regression.fit_exponential(sliced_times, sliced_values)
        target.value = scale
