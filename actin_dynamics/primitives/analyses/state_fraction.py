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

class StateFraction(base_classes.Analysis):
    def __init__(self, label=None, sample_period=None, measurement_name=None,
                 window_size=10, **kwargs):
        self.measurement_name = measurement_name

        self.sample_period = sample_period
        self.window_size = window_size

        base_classes.Analysis.__init__(self, label=label, **kwargs)

    def perform(self, simulation_results, result_factory):
        measurement = simulation_results[self.measurement_name]

        m_times = numpy.array(measurement.get_times())
        m_means = numpy.array(measurement.get_means())

        output_times = numpy.arange(m_times[0], m_times[-1],
                self.sample_period * self.window_size)


        num_rows = int(len(m_times) / self.window_size)
        reshaped = m_means[:num_rows * self.window_size].reshape(num_rows,
                self.window_size)
        output_means = map(numpy.mean, reshaped)

        output_errors = numpy.zeros(len(output_times))

        return result_factory((output_times, output_means, output_errors),
                self.label)
