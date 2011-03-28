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

from actin_dynamics.numerical import interpolation, workalike, measurements, histograms, regression, residuals

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

        # Amount to shift to find fluctuations.
        delta = int(self.tau / self.sample_period)

        fluctuations = []
        for measurement in sampled_measurements:
            subtracted_measurement = _remove_velocity(measurement)
            sliced_measurement = measurements.time_slice(subtracted_measurement,
                                                         self.start_time,
                                                         self.stop_time)
            filament_fluctuations = _extract_fluctuations(sliced_measurement,
                                                          delta)
            fluctuations.extend(filament_fluctuations)

        # Make histogram
        histogram = histograms.make_histogram(fluctuations, self.bin_size)
#        _log.warn('histo x: %s', histogram[0])
#        _log.warn('histo y: %s', histogram[1])

        return result_factory(histogram, label=self.label)


def _remove_velocity(measurement):
    times  = numpy.array(measurement[0])
    values = numpy.array(measurement[1])

    slope = regression.fit_zero_line(times, values)
    intercept = values[0]

#    _log.warn('times: %s', times)
#    _log.warn('values: %s', values)
#    resid = residuals.naked_chi_squared(measurement,
#        (times, (slope * times) + intercept))
#    _log.warn('slope = %s, intercept = %s, resid = %s', slope, intercept, resid)

    return times, values - (slope * times + intercept)


def _extract_fluctuations(measurement, delta):
    results = []
    values = measurement[1]
    if len(values) < delta:
        _log.error('Tau too large:  delta = %s, length = %s.',
                    delta, len(values))

    shifted = numpy.roll(values, delta)
    difference = values[delta:] - shifted[delta:]
    results.extend(list(difference))
    return results
