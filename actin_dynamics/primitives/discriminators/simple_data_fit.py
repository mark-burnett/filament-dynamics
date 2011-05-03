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

from .base_classes import Comparator

from actin_dynamics.numerical import residuals
from actin_dynamics.numerical import interpolation
from actin_dynamics.numerical import measurements
import itertools

from actin_dynamics import logger
log = logger.getLogger(__file__)

class TimecourseFit(Comparator):
    def __init__(self, measurement=None, residual_type=None,
                 interpolate_simulation=True, label=None,
                 scale_simulation_by=1):
        self.residual_function      = getattr(_residuals, residual_type)
        self.measurement_name       = measurement
        self.interpolate_simulation = bool(interpolate_simulation)
        self.scale_simulation_by    = float(scale_simulation_by)

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        log.debug('Performing SimpleDataFit of %s.', self.measurement_name)
        sim_result = run.analyses[self.measurement_name]
        data = run.experiment.objectives[self.label].measurement
        sim_result = _measurements.scale(sim_result,
                                                  self.scale_simulation_by)
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