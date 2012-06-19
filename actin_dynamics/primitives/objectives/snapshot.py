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

from . import base_classes

from actin_dynamics.numerical import measurements

class Snapshot(base_classes.Objective):
    def __init__(self, time=None, analysis_name=None, secondary_name=None,
            subtract_first=0, scale_by=1, divide_by=1,
            average=False, *args, **kwargs):
        self.time = float(time)
        self.average = average
        self.analysis_name = analysis_name
        self.secondary_name = secondary_name

        self.subtract_first = subtract_first
        self.scale_by = scale_by
        self.divide_by = divide_by

        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        results = [run.analyses[self.analysis_name]]
        if self.secondary_name:
            results.append(run.analyses[self.secondary_name])

        times, values, errors = measurements.add(results)

        i = bisect.bisect_left(times, self.time)
        if not self.average:
            value = values[i]
        else:
            value = numpy.mean(values[i:])

        value -= self.subtract_first
        value *= self.scale_by
        value /= self.divide_by
        target.value = value
