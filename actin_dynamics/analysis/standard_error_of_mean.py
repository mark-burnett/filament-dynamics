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

import collections
import math
import operator

from . import utils


def all_measurements(simulations):
    analysis = {}
    for name, measurements in concentration_measurements(simulations).iteritems():
        analysis[name] = calculate_sem_trace(measurements)

    for name, measurements in filament_measurements(simulations).iteritems():
        analysis[name] = calculate_sem_trace(measurements)

    return analysis


def calculate_sem_trace(measurements):
    '''
    Workhorse function.  Calculates the standard error of the mean.
    '''
    sqrt_N = math.sqrt(len(measurements))
    values = map(operator.itemgetter(1), measurements)
    transposed_values = zip(*values)

    means  = []
    errors = []
    for tv in transposed_values:
        mean = sum(tv) / len(tv)
        err  = math.sqrt(sum((v - mean)**2 for v in tv) / len(tv)) / sqrt_N
        means.append(mean)
        errors.append(err)

    times = measurements[0][0]

    return times, means, errors


def concentration_measurements(simulations):
    results = collections.defaultdict(list)
    for simulation in simulations:
        for name, measurement in simulation['concentrations'].iteritems():
            results[name].append(measurement)
    return results


def filament_measurements(simulations):
    results = collections.defaultdict(list)
    for filament in utils.iter_filaments(simulations):
            for name, measurement in filament['measurements'].iteritems():
                results[name].append(measurement)
    return results
