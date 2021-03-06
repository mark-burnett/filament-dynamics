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

from .base_classes import Objective as _Objective

from actin_dynamics.numerical import residuals as _residuals
from actin_dynamics.numerical import interpolation as _interpolation
from actin_dynamics.numerical import measurements as _measurements
import itertools as _itertools

from actin_dynamics import logger
log = logger.getLogger(__file__)

class SimpleDataFit(_Objective):
    def __init__(self, measurement=None, residual_type=None,
                 interpolate_simulation=False, label=None,
                 skip_beginning=0, scale_simulation_by=1):
        self.residual_function      = getattr(_residuals, residual_type)
        self.measurement_name       = measurement
        self.interpolate_simulation = bool(interpolate_simulation)
        self.scale_simulation_by    = float(scale_simulation_by)
        self.skip_beginning = float(skip_beginning)

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        log.debug('Performing SimpleDataFit of %s.', self.measurement_name)
        sim_result = run.analyses[self.measurement_name]
        data = run.experiment.objectives[self.label].measurement
        sim_result = _measurements.skip_beginning(sim_result,
                self.skip_beginning)
        sim_result = _measurements.scale(sim_result, self.scale_simulation_by)

        if self.interpolate_simulation:
            interp = _interpolation.resample_measurement(sim_result, data[0])

#            log.debug('interp times: %s', interp[0])
            log.debug('Sim  values: %s', interp[1])
            log.debug('Data values: %s', data[1])

            target.value = self.residual_function(interp, data)
        else:
            target.value = self.residual_function(sim_result, data)

            log.debug('Sim  values: %s', sim_result[1])
            log.debug('Data values: %s', data[1])
        log.debug('Objective value: %s.', target.value)

        if target.value <= 0:
            log.warn('Negative or zero residual found %s.', target.value)

class HalftimeFit(_Objective):
    def __init__(self, measurement=None, base_value=None,
            data_halftime=None, label=None):
        self.measurement_name = measurement
        self.data_halftime = float(data_halftime)
        self.half_value = float(base_value) / 2

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        sim_result = run.analyses[self.measurement_name]
        times, values, errors = sim_result
        halftime = _calc_halftime(times, values, self.half_value)

        target.value = (halftime - self.data_halftime)**2


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

    y = _interpolation.linear_project(left_value, left_time,
            right_value, right_time, half_value)

    if y == float('nan'):
        log.error('Halftime is not a number: i = %s, lt = %s, rt = %s, lv = %s, rv = %s',
                i, left_time, right_time, left_value, right_value)
    return y
