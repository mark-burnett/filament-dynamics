#    Copyright (C) 2010-2011 Mark Burnett
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

from ..meta_classes import Registration

from registry import measurement_registry


def _datastore_factory():
    return [], []


class Measurement(object):
    __metaclass__ = Registration
    registry = measurement_registry
    skip_registration = True

    __slots__ = ['label']
    def __init__(self, label=None):
        self.label = label


class FilamentMeasurement(Measurement):
    skip_registration = True
     __slots__ = ['_datastore']
     def __init__(self, *args, **kwargs):
         Measurement.__init__(self, *args, **kwargs)

    def initialize(self, results):
        self._datastore = collections.defaultdict(_datastore_factory)
        results['filaments'][self.label] = self._datastore

    def store(self, time, value, filament_name):
        result_times, result_values = self._datastore[filament_name]
        result_times.append(time)
        result_values.append(state_count)


class ConcentrationMeasurement(Measurement):
     __slots__ = ['_datastore', '_data_times', '_data_values']
     def __init__(self, *args, **kwargs):
         Measurement.__init__(self, *args, **kwargs)

    def initialize(self, results):
        self._datastore = _datastore_factory()
        self._data_times, self._data_values = self._datastore
        results['concentrations'][self.label] = self._datastore

    def store(self, time, value):
        self._data_times.append(time)
        self._data_values.append(state_count)

    def perform(self, time, simulation_state):
        self.store(time, simulation_state.concentrations[self.label])
