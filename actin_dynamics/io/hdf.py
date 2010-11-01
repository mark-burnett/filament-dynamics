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

import gc
import itertools

import tables

import hdf_format

class Writer(object):
    def __init__(self, file_name):
        self.hdf_file    = tables.openFile(file_name, mode='w')
        self.simulations = self.hdf_file.createGroup('/', 'Simulations',
                                                     'Raw Simulation Data')

    def __del__(self):
        self.hdf_file.close()

    def write_result(self, result):
        (parameters, simulation_measurements,
            raw_filaments, filament_measurements) = result

        num_written_simulations = len(self.simulations._v_children)

        result_group = self.hdf_file.createGroup(self.simulations,
                                                 ('simulation_%s' %
                                                     num_written_simulations))

        self._save_parameters(parameters, result_group)

        sim_measurement_group = self.hdf_file.createGroup(result_group,
                'simulation_measurements')
        self._save_measurement_collection(collection=simulation_measurements,
                                          group=sim_measurement_group)

        self._save_filament_data(states=raw_filaments,
                                 measurement_collections=filament_measurements,
                                 group=result_group)


    def _save_parameters(self, parameters, result_group):
        table = self.hdf_file.createTable(result_group, 'parameters', hdf_format.Parameter,
                                  'Simulation Parameters')
        row = table.row
        for name, value in parameters.iteritems():
            row['name']  = name
            row['value'] = value
            row.append()

        table.flush()

    def _save_measurement_collection(self, collection=None, group=None, **kwargs):
        for name, measurements in collection.iteritems():
            sub_group = self.hdf_file.createGroup(group, name)
            self._save_measurements(measurements=measurements, group=sub_group,
                                    **kwargs)

    def _save_measurements(self, measurements=None, group=None, table_name='data'):
        table = self.hdf_file.createTable(group, table_name, hdf_format.Measurement)

        row = table.row
        for time, value in measurements:
            row['time']  = time
            row['value'] = value
            row.append()

        table.flush()

    def _save_filament_data(self, states=None, measurement_collections=None,
                            group=None):
        for i, (st, mc) in enumerate(itertools.izip(states, measurement_collections)):
            filament_group = self.hdf_file.createGroup(group, 'filament_%s' % i)
            self._save_filament_state(states=st, group=filament_group,
                                      table_name='final_states')
            self._save_measurement_collection(collection=mc,
                                              group=filament_group)

    def _save_filament_state(self, states=None, group=None, table_name='states'):
        table = self.hdf_file.createTable(group, table_name, hdf_format.State)
        row = table.row
        for s in states:
            row['state'] = s
            row.append()

        table.flush()
