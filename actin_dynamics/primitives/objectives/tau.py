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
    def __init__(self, analysis_name=None, falling=False, *args, **kwargs):
        self.analysis_name = analysis_name
        self.falling = falling
        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        times, values, errors = run.analyses[self.analysis_name]

        target.value = _calc_halftime(times, values, self.falling)

def _calc_halftime(times, values, falling):
    max_val = max(values)
    max_index = values.index(max_val)

    if falling:
        raise NotImplementedError()
    else:
        cut_vals = values[:max_index+1]
        min_val = values[0]
        half_val = (max_val - min_val) / 2

        i = bisect.bisect_left(cut_vals, half_val)

        left_time = times[i]
        left_value = values[i]

        right_time = times[i+1]
        right_value = values[i+1]

        return interpolation.linear_project(left_value, left_time,
                right_value, right_time, half_val)


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
