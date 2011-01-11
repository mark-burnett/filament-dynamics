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

import numpy


def all_measurements(parameter_sets, source='downsampled'):
    analysis = {}
    for parameter_set in parameter_sets:
        for name, values in concentration_measurements(parameter_set):
            analysis[name] = calculate_sem_trace(values)

        for name, values in filament_measurements(parameter_set):
            analysis[name] = calculate_sem_trace(values)

    return analysis


def calculate_sem_trace(measurements):
    '''
    Workhorse function.  Calculates the standard error of the mean.
    '''
    values = map(operator.itemgetter(1), measurements)
    sqrt_N = math.sqrt(len(values))
    transposed_values = numpy.array(values).transpose()

    means  = []
    errors = []
    for tv in transposed_values:
        means.append(numpy.average(tv))
        errors.append(numpy.std(tv) / sqrt_N)

    times = measurements[0][0]

    return times, means, errors

def concentration_measurements(parameter_set):
    results = collections.defaultdict(list)
    for simulation in parameter_set:
        for name, measurement in simulation['concentrations'].iteritems():
            results[name].append(measurement)

def filament_measurements(parameter_set):
    results = collections.defaultdict(list)
    for simulation in parameter_set:
        for filament in simulation['filaments']:
            for name, measurement in filament['measurements'].iteritems():
                results[name].append(measurement)
