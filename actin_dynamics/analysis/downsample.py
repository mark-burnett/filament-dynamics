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

import numpy

from . import interpolation

def all_measurements(parameter_set, sample_period=1, epsilon=1e-10,
                     source='simulations'):
    analysis = []
    for simulation in parameter_set[source]:
        sample_times = numpy.arange(0,
                parameter_set['parameters']['simulation_duration'] + epsilon,
                sample_period)

        sim_results = {}

        # Downsample concentrations.
        sim_results['concentrations'] = collection_measurements(
                simulation['concentrations'], sample_times)

        # Downsample individual filament measurements.
        filament_results = []
        for filament in simulation['filaments']:
            fr = {}
            fr['measurements'] = collection_measurements(
                    filament['measurements'], sample_times)
            filament_results.append(fr)
        sim_results['filaments'] = filament_results

        analysis.append(sim_results)

    return analysis



def collection_measurements(measurements, sample_times):
    results = {}
    for name, values in measurements.iteritems():
        results[name] = interpolation.resample_measurement(
                values, sample_times, method='previous_value')
    return results
