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

import tables

from . import wrappers as _wrappers

class SimulationReader(object):
    def __init__(self, simulation_group=None):
        self.simulation_group = simulation_group

    def collect_filament_measurements(self, name):
        results = []
        for filament in self.simulation_group.filaments:
            results.append(self.get_measurement(name, filament.measurements))
        return results

    def get_measurement(self, name, group=None):
        if group is None:
            g = self.simulation_group.simulation_measurements
        table = getattr(g, name)
        m = _wrappers.Measurement(table)
        return m.read()

class MultipleSimulationReader(object):
    def __init__(self, simulations_group=None):
        self.simulations = [SimulationReader(s) for s in simulations_group]

    def collect_simulation_measurements(self, name):
        return self._collect_measurements(name, 'get_measurement')

    def collect_filament_measurements(self, name):
        return self._collect_measurements(name, 'collect_filament_measurements')

    def _collect_measurements(self, name, function):
        results = []
        for s in self.simulations:
            f = getattr(s, function)
            results.append(f(name))
        return results

class AnalysisReader(object):
    pass
