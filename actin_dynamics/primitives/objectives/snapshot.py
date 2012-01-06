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
    def __init__(self, time=None, analysis_name=None,
            secondary_name=None, average=False, *args, **kwargs):
        self.time = float(time)
        self.average = average
        self.analysis_name = analysis_name
        self.secondary_name = secondary_name

        base_classes.Objective.__init__(self, *args, **kwargs)

    def perform(self, run, target):
        results = [run.analyses[self.analysis_name]]
        if self.secondary_name:
            results.append(run.analyses[self.secondary_name])

        times, values, errors = measurements.add(results)

        i = bisect.bisect_left(times, self.time)
        if not self.average:
            target.value = values[i]
        else:
            target.value = numpy.mean(values[i:])
