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

from actin_dynamics import logger as _logger

_log = _logger.getLogger(__file__)

def get_measurement(simulation_results, name, measurement_type):
    if 'filament' == measurement_type:
        iterator = iter_filaments(simulation_results)
        measurement_key = 'measurements'
    else:
        iterator = simulation_results
        measurement_key = 'concentrations'

    results = []
    for item in iterator:
        results.append(item[measurement_key][name])
    return results


def iter_filaments(simulation_results):
    for simulation in simulation_results:
        for filament in simulation['filaments']:
            yield filament

def get_concentration_measurements(simulation_results, name):
    return [sr['concentrations'][name] for sr in simulation_results]

def get_measurement_bundle(simulation_results, name):
    bundle = []
    for simulation in simulation_results:
        measurements = [f['measurements'][name] for f in simulation['filaments']]
        bundle.append(measurements)
    return bundle
