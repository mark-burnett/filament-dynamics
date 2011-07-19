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


def _calc_halftime(times, values, half_value):
    i = bisect.bisect_left(values, half_value)

    left_time = times[i]
    left_value = values[i]

    # XXX This obviously breaks if the halftime isn't reached.
    right_time = times[i+1]
    right_value = values[i+1]

    return interpolation.linear_project(left_value, left_time,
            right_value, right_time, half_value)


class PeakTime(base_classes.Objective):
    def __init__(self, analysis_name=None, *args, **kwargs):
        self.analysis_name = analysis_name
        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        times, values, errors = run.analyses[self.analysis_name]

        max_value = max(values)
        max_index = values.index(max_value)
        target.value = times[max_index]


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
