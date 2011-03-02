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

import math
import operator

from . import base_classes as _base_classes

from . import utils

from actin_dynamics.numerical import interpolation, workalike

from actin_dynamics import logger as _logger

_log = _logger.getLogger(__file__)

class StandardErrorMean(_base_classes.Analysis):
    def __init__(self, sample_period=None, stop_time=None,
                 interpolation_method=None, measurement_name=None,
                 measurement_type=None, label=None, **kwargs):
        self.sample_period        = sample_period
        self.stop_time            = stop_time
        self.interpolation_method = interpolation_method
        self.measurement_name     = measurement_name
        self.measurement_type     = measurement_type

        _base_classes.Analysis.__init__(self, label=label, **kwargs)

    def perform(self, simulation_results, result_factory):
        # Grab and resample the chosen measurement.
        raw_measurements = utils.get_measurement(simulation_results,
                                                 self.measurement_name,
                                                 self.measurement_type)
        sample_times = workalike.arange(0, self.stop_time,
                                        self.sample_period)
        if not sample_times:
            _log.error('Sample time length is 0.  ' +
                       'Measurement name: %s, stop_time: %s, period %s.',
                       self.measurement_name, self.stop_time,
                       self.sample_period)
        sampled_measurements = [interpolation.resample_measurement(
            rm, sample_times, method=self.interpolation_method)
                for rm in raw_measurements]

        # Perfom SEM analysis on that measurement
        resulting_measurement = _calculate_sem(sampled_measurements)

        # Create and return result object.
        return result_factory(resulting_measurement, label=self.label)


def _calculate_sem(measurements):
    sqrt_N = math.sqrt(len(measurements))
    values = map(operator.itemgetter(1), measurements)
    transposed_values = zip(*values)

    means  = []
    errors = []
    for tv in transposed_values:
        mean = sum(tv) / len(tv)
        err = workalike.std(tv, mean) / sqrt_N
        means.append(mean)
        errors.append(err)

    times = measurements[0][0]

    return times, means, errors
