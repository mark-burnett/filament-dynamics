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

from . import table_wrappers as _table_wrappers
from . import base_group_wrappers as _base_group_wrappers
from . import table_formats as _table_formats

class MeasurementCollection(_base_group_wrappers.Collection):
    child_wrapper = _table_wrappers.Measurement

class FilamentWrapper(_base_group_wrappers.GroupWrapper):
    def __iter__(self):
        return _base_group_wrappers._WrappedIterator(self.group.measurements,
                _table_wrappers.Measurement)

class SimulationWrapper(_base_group_wrappers.GroupWrapper):
    def __iter__(self):
        return _base_group_wrappers._WrappedIterator(self.group.filaments,
                                                     FilamentWrapper)

    def __getitem__(self, simulation_measurement_name):
        return _table_wrappers.Measurement(
                getattr(self.group.simulation_measurements,
                        simulation_measurement_name))

class ParameterSetWrapper(_base_group_wrappers.GroupWrapper):
    def __init__(self, group=None):
        self.parameters = _table_wrappers.Parameters(group.parameters)
        _base_group_wrappers.GroupWrapper.__init__(self, group)

    def __iter__(self):
        return _base_group_wrappers._WrappedIterator(self.group.simulations,
                                                     SimulationWrapper)

    def __getitem__(self, key):
        return self.parameters[key]

class MultipleParameterSetWrapper(_base_group_wrappers.Collection):
    child_wrapper = ParameterSetWrapper

class MultipleAnalysisWrapper(_base_group_wrappers.Collection):
    child_wrapper = MultipleParameterSetWrapper
