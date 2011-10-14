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

import itertools
import math
import operator

import numpy

from . import base_classes as _base_classes

from . import utils

from actin_dynamics.numerical import interpolation, workalike, measurements

from actin_dynamics import logger as _logger
_log = _logger.getLogger(__file__)

class StandardErrorMean(_base_classes.Analysis):
    def __init__(self, sample_period=None, stop_time=None,
                 interpolation_method=None, measurement_name=None,
                 measurement_type=None, label=None,
                 scale_by=1, add=0, subtract=0, **kwargs):
        self.sample_period        = float(sample_period)
        self.stop_time            = float(stop_time)
        self.interpolation_method = interpolation_method
        self.measurement_name     = measurement_name
        self.measurement_type     = measurement_type

        self.scale_by = float(scale_by)
        self.add      = float(add)
        self.subtract = float(subtract)

        _base_classes.Analysis.__init__(self, label=label, **kwargs)

    def perform(self, simulation_results, result_factory):
        if 'concentration' == self.measurement_type:
            return self.perform_concentration(simulation_results, result_factory)
        elif 'filament' == self.measurement_type:
            return self.perform_filament(simulation_results, result_factory)

    def perform_concentration(self, simulation_results, result_factory):
        raw_measurements = utils.get_concentration_measurements(
                simulation_results, self.measurement_name)
        rescaled_measurements = self._rescale_concentration_measurements(
                raw_measurements)

        resulting_measurement = _calculate_concentration_sem(
                rescaled_measurements)

        return result_factory(resulting_measurement, label=self.label)

    def _rescale_concentration_measurements(self, raw_measurements):
        scaled_measurements = [measurements.scale(sm, self.scale_by)
                               for sm in raw_measurements]
        added_measurements  = [measurements.add_number(sm, self.add)
                               for sm in scaled_measurements]

        subtracted_measurements  = [measurements.add_number(am,
                                        -self.subtract)
                                    for am in added_measurements]
        return subtracted_measurements


    def perform_filament(self, simulation_results, result_factory):
        # Grab and resample the chosen measurement.
        raw_measurements = utils.get_measurement_bundle(simulation_results,
                self.measurement_name)
        rescaled_measurements = self._rescale_filament_measurements(
                raw_measurements)

        resulting_measurement = _calculate_filament_sem(rescaled_measurements)

        return result_factory(resulting_measurement, label=self.label)

    def _rescale_filament_measurements(self, raw_measurements):
        result_bundle = []
        for simulation in raw_measurements:
            scaled_measurements = [measurements.scale(sm, self.scale_by)
                                   for sm in simulation]
            added_measurements  = [measurements.add_number(sm, self.add)
                                   for sm in scaled_measurements]

            subtracted_measurements  = [measurements.add_number(am,
                                            -self.subtract)
                                        for am in added_measurements]
            result_bundle.append(subtracted_measurements)
        return result_bundle


def _calculate_concentration_sem(measurements):
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

def _calculate_filament_sem(measurements):
    times, means, stds, Ns = _bundle_stats(measurements)
#    sqrt_N = math.sqrt(sum(Ns))
    values = []
    errors = []
    for i, t in enumerate(times):
        v, e = _single_point_sem(means, stds, i, Ns)
        values.append(v)
        errors.append(e)

    return times, values, errors

def _single_point_sem(means, stds, Ns, index):
    value_components = []
    error_components = []
    num_components = []
    for m, s, n in itertools.izip(means, stds, Ns):
        if index < len(m):
            value_components.append(m[i])
            ec = (n - 1) * (s[i]**2) - n * m[i]**2
            error_components.append(s[i])
            num_components.append(n)

    value = numpy.mean(value_components)

    N = sum(num_components)
    combined_std = math.sqrt((sum(error_components) + N * value**2) / (N - 1))

    error = value * combined_std / math.sqrt(N)
    return value, error


def _bundle_stats(bundle):
    times = []
    means = []
    stds = []
    Ns = []
    for measurements in bundle:
        t = measurements[0][0]
        values = []
        N = 0
        for measurement in measurements:
            N += 1
            values.append(measurement[1])
        ta = numpy.array(values).transpose()
        m = [numpy.mean(tax) for tax in ta]
        s = [numpy.std(tax) for tax in ta]
        times.append(t)
        means.append(m)
        stds.append(s)
        Ns.append(N)

    combined_times = []
    for t in times:
        if len(t) > len(combined_times):
            combined_times = t

    return combined_times, means, stds, Ns
