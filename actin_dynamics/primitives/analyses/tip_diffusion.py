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

from actin_dynamics.numerical import interpolation, workalike, regression

from actin_dynamics import logger as _logger
_log = _logger.getLogger(__file__)

class FluctuationVariances(_base_classes.Analysis):
    def __init__(self, start_time=None, stop_time=None, sample_period=None,
                 tau_min=None, tau_max=None,
                 interpolation_method=None,
                 measurement_name='length', measurement_type='filament',
                 label=None):
        self.start_time           = float(start_time)
        self.stop_time            = float(stop_time)
        self.sample_period        = float(sample_period)

        self.tau_min              = float(tau_min)
        self.tau_max              = float(tau_max)

        self.interpolation_method = interpolation_method
        self.measurement_name     = measurement_name
        self.measurement_type     = measurement_type

        _base_classes.Analysis.__init__(self, label=label)

    def perform(self, simulation_results, result_factory):
        fluctuations = self.get_fluctuations(simulation_results)
        taus = range(self.tau_min, self.tau_max + self.sample_period/2,
                     self.sample_period)
        variances = []
        for tau in taus:
            local_fluctuations = []
            for measurement in fluctuations:
                local_fluctuations.extend(_calculate_local_fluctuations(
                    measurement, tau, self.sample_period))
            variances.append(numpy.var(local_fluctuations))

        errors = [0 for tau in taus]
        return result_factory((taus, variances, errors), label=self.label)

    def get_fluctuations(self, simulation_results):
        sampled_measurements = self.get_sampled_measurements(simulation_results)
        return [_remove_velocity(sm) for sm in sampled_measurements]

    def get_sampled_measurements(self, simulation_results):
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
        return [interpolation.resample_measurement(
           rm, sample_times, method=self.interpolation_method)
               for rm in raw_measurements]


def _remove_velocity(measurement):
    times  = numpy.array(measurement[0])
    values = numpy.array(measurement[1])

    slope = regression.fit_zero_line(times, values)
    intercept = values[0]

    return times, values - (slope * times + intercept)

def _calculate_local_fluctuations(measurement, tau, sample_period):
    results = []
    values = measurement[1]
    delta = int(tau / sample_period)
    if delta * sample_period != tau:
        _log.error('tau not divisible by sample_period: %s / %s',
                   tau, sample_period)

    if len(values) < delta:
        _log.error('Delta too large:  tau = %s, delta = %s, length = %s.',
                    tau, delta, len(values))

    return list(values[delta:] - values[:-delta])
