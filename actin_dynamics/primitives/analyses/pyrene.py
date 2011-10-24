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

import numpy

from . import base_classes as _base_classes

from . import utils

from actin_dynamics.numerical import interpolation, measurements

from actin_dynamics import logger as _logger
_log = _logger.getLogger(__file__)

class PyreneSEM(_base_classes.Analysis):
    def __init__(self, sample_period=None, stop_time=None, label=None,
                 **kwargs):
        self.sample_period        = float(sample_period)
        self.stop_time            = float(stop_time)

        self.weights = dict((k, float(v)) for k, v in kwargs.iteritems())

        _base_classes.Analysis.__init__(self, label=label, **kwargs)

    def perform(self, simulation_results, result_factory):
        pyrene_measurements = [self._get_pyrene_measurements(s)
                for s in simulation_results]
        resulting_measurement = _calculate_concentration_sem(pyrene_measurements)

        return result_factory(resulting_measurement, label=self.label)

    def _get_pyrene_measurements(self, simulation):
        # Loop over each weight,
        times = numpy.arange(0, self.stop_time, self.sample_period)
        total = []
        for name, weight in self.weights.iteritems():
            raw = [f['measurements'][name] for f in simulation['filaments']]
            interpolated = []
            for rm in raw:
                junk_times, values = interpolation.resample_measurement(rm, times,
                        method='previous_value')
                values = numpy.array(values)
                if 0 == len(interpolated):
                    interpolated = values
                else:
                    interpolated += values
            interpolated *= weight
            if 0 == len(total):
                total = interpolated
            else:
                total += interpolated

        return times, total


def _calculate_concentration_sem(measurements):
    all_times, all_values = zip(*measurements)

    times = []
    for ts in all_times:
        if len(ts) > len(times):
            times = ts

    means = []
    errors = []
    for i, t in enumerate(times):
        mean, error = _stats(all_values, i)
        means.append(mean)
        errors.append(error)

    return times, means, errors


def _stats(values, index):
    set_values = []
    for vs in values:
        if len(vs) > index:
            set_values.append(vs[index])

    m = numpy.mean(set_values)
    s = numpy.std(set_values)

    return m, s / numpy.sqrt(len(set_values))


#def _calculate_filament_sem(measurements):
#    times, means, stds, Ns = _bundle_stats(measurements)
#    values = []
#    errors = []
#    for i, t in enumerate(times):
#        v, e = _single_point_sem(means, stds, Ns, i)
#        values.append(v)
#        errors.append(e)
#
#    return times, values, errors
#
#def _single_point_sem(means, stds, Ns, index):
#    value_components = []
#    error_components = []
#    num_components = []
#    for m, s, n in itertools.izip(means, stds, Ns):
#        if index < len(m):
#            value_components.append(m[index])
#            ec = (n - 1) * (s[index]**2) - n * m[index]**2
#            error_components.append(s[index])
#            num_components.append(n)
#
#    value = numpy.mean(value_components)
#
#    N = sum(num_components)
#    combined_std = math.sqrt((sum(error_components) + N * value**2) / (N - 1))
#
#    error = value * combined_std / math.sqrt(N)
#    return value, error
#
#
#def _bundle_stats(bundle):
#    times = []
#    means = []
#    stds = []
#    Ns = []
#    for measurements in bundle:
#        t = measurements[0][0]
#        values = []
#        N = 0
#        for measurement in measurements:
#            N += 1
#            values.append(measurement[1])
#        ta = numpy.array(values).transpose()
#        m = [numpy.mean(tax) for tax in ta]
#        s = [numpy.std(tax) for tax in ta]
#        times.append(t)
#        means.append(m)
#        stds.append(s)
#        Ns.append(N)
#
#    combined_times = []
#    for t in times:
#        if len(t) > len(combined_times):
#            combined_times = t
#
#    return combined_times, means, stds, Ns
