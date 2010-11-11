#    Copyright (C) 2010 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify #    it under the terms of the GNU General Public License as published by
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

import itertools

import tables

from . import wrappers as _wrappers

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


        par_table = _wrappers.Parameters.in_group(hdf_file=self.hdf_file,
                                                  parent_group=result_group)
        par_table.write(parameters)

        sm_group = _wrappers.MeasurementCollection.in_group(
                hdf_file=self.hdf_file, parent_group=result_group,
                name='simulation_measurements')
        sm_group.write(simulation_measurements)

        filament_group = self.hdf_file.createGroup(result_group,
                'filaments')

        for i, (fm, states) in enumerate(itertools.izip(filament_measurements,
                                                        raw_filaments)):
            fg = self.hdf_file.createGroup(filament_group,
                                           name=('filament_%s' % i))
            fil_col = _wrappers.MeasurementCollection.in_group(
                    hdf_file=self.hdf_file, parent_group=filaments,
                    name='measurements')
            fil_col.write(fm)

            state = _wrappers.State.in_group(hdf_file=self.hdf_file,
                    parent_group=fg, name='final_state')
            state.write(states)
