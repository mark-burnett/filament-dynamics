#    Copyright (C) 2012 Mark Burnett
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

import numpy

from . import base_classes

#from actin_dynamics import logger as _logger
#_log = _logger.getLogger(__file__)

class StandardErrorMean(base_classes.Analysis):
    def __init__(self, sample_period=None, stop_time=None,
                 measurement_name=None, measurement_type=None, label=None,
                 scale_by=1, add=0, subtract=0, number_of_filaments=1,
                 **kwargs):
        self.measurement_name = measurement_name

        self.scale_by = float(scale_by)
        self.add      = float(add)
        self.subtract = float(subtract)

        self.number_of_filaments = number_of_filaments

        _base_classes.Analysis.__init__(self, label=label, **kwargs)

    def perform(self, simulation_results, result_factory):
        measurement = simulation_results[self.measurement_name]

        times = numpy.array(measurement.get_times())

        means = numpy.array(measurement.get_means())
        means *= self.scale_by
        means += self.add - self.subtract

        errors = numpy.array(measurement.get_errors(self.number_of_filaments))
        errors *= self.scale_by

        return result_factory((times, means, errors))
