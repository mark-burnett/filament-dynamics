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

from . import base_classes as _base_classes

import numpy
from actin_dynamics.numerical import correlation, interpolation

from actin_dynamics import logger
log = logger.getLogger(__file__)


class ThresholdVelocityAutocorrelation(_base_classes.Analysis):
    def __init__(self, std_devs=None, measurement_name=None, side='above',
            sample_period=None, start_time=0, stop_time=None,
            *args, **kwargs):
        self.std_devs = float(std_devs)
        self.measurement_name = measurement_name
        self.side = side

        self.sample_period = sample_period
        self.start_time = start_time
        self.stop_time = stop_time

        _base_classes.Analysis.__init__(self, *args, **kwargs)

    def perform(self, simulation_results, result_factory):
        value_collection = []
#        sample_period = None
        sample_times = numpy.arange(self.start_time,
                self.stop_time + self.sample_period/2, self.sample_period)
        for simulation in simulation_results:
            times, values = simulation['filaments'][0]['measurements'
                    ][self.measurement_name]
            stimes, sampled_values = interpolation.resample_measurement(
                    (times, values), sample_times, method='previous_value')

#            if not sample_period and len(times) > 1:
#                sample_period = float(times[1] - times[0])
            value_collection.append(sampled_values)

        # calculate velocities collection
        velocity_collection = [numpy.diff(v) / self.sample_period
                for v in value_collection]

        # collection get mean/std -> threshold
        mean, std = correlation.collection_stats(velocity_collection)
        threshold = mean + self.std_devs * std

        # do autocorrelation
        if 'above' == self.side.lower():
            matched_collection = [numpy.array(velocities > threshold, dtype=int)
                    for velocities in velocity_collection]
        else:
            matched_collection = [numpy.array(velocities < threshold, dtype=int)
                    for velocities in velocity_collection]

        measurement = correlation.aggregate_autocorrelation(self.sample_period,
                matched_collection)

        return result_factory(measurement, label=self.label)
