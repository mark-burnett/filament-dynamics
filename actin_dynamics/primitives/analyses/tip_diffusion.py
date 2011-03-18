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

import numpy

from . import base_classes as _base_classes

from . import utils

from actin_dynamics.numerical import interpolation, workalike, measurements, histograms

from actin_dynamics import logger as _logger

_log = _logger.getLogger(__file__)

class TipDiffusionHistogram(_base_classes.Analysis):
    def __init__(self, sample_period=None, start_time=None, stop_time=None,
                 interpolation_method=None,
                 measurement_name='length', measurement_type='filament',
                 label=None, bin_size=None, tau=None, **kwargs):
        self.sample_period        = float(sample_period)
        self.start_time           = float(start_time)
        self.stop_time            = float(stop_time)
        self.interpolation_method = interpolation_method
        self.measurement_name     = measurement_name
        self.measurement_type     = measurement_type
        self.bin_size             = float(bin_size)
        self.tau                  = float(tau)

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

        # Remove first order changes (average growth)
        velocity_subtracted_values = _remove_velocity(sampled_measurements,
                                                      self.start_time,
                                                      self.stop_time)

        # Extract fluctuations
        delta = int(self.tau / self.sample_period)
        fluctuations = _extract_fluctuations(velocity_subtracted_values, delta)

        # Make histogram
        histogram = histograms.make_histogram(fluctuations, self.bin_size)

        return result_factory(histogram, label=self.label)


def _remove_velocity(sampled_measurements, start_time, stop_time):
    results = []
    for m in sampled_measurements:
        sliced_measurement = measurements.time_slice(m, start_time, stop_time)

        values = sliced_measurement[1]
        discrete_slope = float(values[-1] - values[0]) / len(values)

        results.append(numpy.array([v - i * discrete_slope
                                    for i, v in enumerate(values)]))
    return results


def _extract_fluctuations(values, delta):
    results = []
    for v in values:
        shifted = numpy.roll(v, delta)
        difference = shifted[delta:] - v[delta:]
        results.extend(list(difference))
    return results
