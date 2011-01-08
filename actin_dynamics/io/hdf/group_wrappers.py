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

    def create_filament(self, name):
        return self.create_subgroup(name=name, wrapper=FilamentWrapper)

    @property
    def simulation_measurements(self):
        return MeasurementCollection.create_or_select(
                self._pytables_object,
                'simulation_measurements')

    @property
    def filament_measurements(self):
        return MeasurementCollection.create_or_select(
                self._pytables_object,
                'filament_measurements')

    def write_measurements(self, results_dict):
        self.simulation_measurements.write(results_dict)

    @property
    def filaments(self):
        return FilamentCollection.create_or_select(
                self._pytables_object, 'filaments')

    @property
    def filament_measurement_names(self):
        first_filament = next(iter(self.filaments))
        return [m.name for m in first_filament.measurements]

class SimulationCollection(_base_group_wrappers.Collection):
    child_wrapper = SimulationWrapper

    def create_child_from_number(self, number):
        return self.create_child(name='simulation_%s' % number)

    def select_child_number(self, number):
        return self.create_or_select_child('simulation_%s' % number)


class ParameterSetWrapper(_base_group_wrappers.GroupWrapper):
    @property
    def simulations(self):
        return SimulationCollection.create_or_select(
                parent_group=self._pytables_object, name='simulations')

    @property
    def parameters(self):
        return _table_wrappers.Parameters.create_or_select(
                parent_group=self._pytables_object)

    @property
    def values(self):
        return _table_wrappers.Values.create_or_select(
                parent_group=self._pytables_object)

    @property
    def measurement_summary(self):
        return MeasurementCollection.create_or_select(
                parent_group=self._pytables_object, name='measurement_summary')

class MultipleParameterSetWrapper(_base_group_wrappers.Collection):
    child_wrapper = ParameterSetWrapper

    def select_child_number(self, number):
        return self.create_or_select_child('parameter_set_%s' % number)

class MultipleAnalysisWrapper(_base_group_wrappers.Collection):
    child_wrapper = MultipleParameterSetWrapper


class FilamentWrapper(_base_group_wrappers.GroupWrapper):
    @property
    def final_state(self):
        return _table_wrappers.State.create(parent_group=self._pytables_object,
                                            name='final_state')
    @property
    def measurements(self):
        return MeasurementCollection.create_or_select(
                parent_group=self._pytables_object, name='measurements')

class FilamentCollection(_base_group_wrappers.Collection):
    child_wrapper = FilamentWrapper

    def create_child_from_number(self, number):
        return self.create_child(name='filament_%s' % number)


class MeasurementCollection(_base_group_wrappers.Collection):
    child_wrapper = _table_wrappers.Measurement

    def __getattr__(self, key):
        return _table_wrappers.Measurement(getattr(self._pytables_object, key))
