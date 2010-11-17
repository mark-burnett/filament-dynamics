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


class SimulationWrapper(_base_group_wrappers.GroupWrapper):
    def __init__(self, group=None):
        _base_group_wrappers.GroupWrapper.__init__(self, group=group)
        MeasurementCollection.create_or_select(group, 'simulation_measurements')
    def __iter__(self):
        return _base_group_wrappers._WrappedIterator(
                self._pytables_object.filaments, FilamentWrapper)

    def __getitem__(self, simulation_measurement_name):
        return _table_wrappers.Measurement(
                getattr(self._pytables_object.simulation_measurements,
                        simulation_measurement_name))

    def create_filament(self, name):
        return self.create_subgroup(name=name, wrapper=FilamentWrapper)

    @property
    def measurements(self):
        return MeasurementCollection.create_or_select(
                self._pytables_object,
                'simulation_measurements')

    def write_measurements(self, results_dict):
        m = MeasurementCollection.create_or_select(
                self._pytables_object,
                'simulation_measurements')
        m.write(results_dict)

    @property
    def filaments(self):
        return FilamentCollection.create_or_select(
                self._pytables_object, 'filaments')


class ParameterSetWrapper(_base_group_wrappers.GroupWrapper):
    def __init__(self, group=None):
        self.parameters = _table_wrappers.Parameters.create_or_select(
                parent_group=group)
        _base_group_wrappers.GroupWrapper.__init__(self, group)

    def __iter__(self):
        return _base_group_wrappers._WrappedIterator(
                self._pytables_object.simulations, SimulationWrapper)

    def __getitem__(self, key):
        return self.parameters[key]


class FilamentWrapper(_base_group_wrappers.GroupWrapper):
    @property
    def measurements(self):
        return MeasurementCollection.create_or_select(
                parent_group=self._pytables_object, name='measurements')

#    def __iter__(self):
#        return _base_group_wrappers._WrappedIterator(
#                self._pytables_object.measurements,
#                _table_wrappers.Measurement)

class FilamentCollection(_base_group_wrappers.Collection):
    child_wrapper = FilamentWrapper


class MeasurementCollection(_base_group_wrappers.Collection):
    child_wrapper = _table_wrappers.Measurement

class MultipleParameterSetWrapper(_base_group_wrappers.Collection):
    child_wrapper = ParameterSetWrapper

class MultipleAnalysisWrapper(_base_group_wrappers.Collection):
    child_wrapper = MultipleParameterSetWrapper
