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

def get_measurement(simulation_results, name, measurement_type):
    if 'filament' == measurement_type:
        iterator = iter_filaments(results)
    else:
        iterator = simulation_results

    results = []
    for item in iterator:
        results.append(item[name])
    return results


def iter_filaments(simulation_results):
    for simulation in simulation_results:
        for filament in simulation['filaments']:
            yield filament

