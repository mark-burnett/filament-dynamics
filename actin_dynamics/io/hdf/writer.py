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

import itertools

import tables

from . import table_wrappers as _table_wrappers
from . import group_wrappers as _group_wrappers

# XXX Consider making this writer a context?
class SimulationWriter(object):
    def __init__(self, hdf_file=None):
        self.hdf_file = hdf_file
        simulations = self.hdf_file.createGroup('/', 'Simulations',
                                                     'Raw Simulation Data')
        self.parameter_sets = _group_wrappers.MultipleParameterSetWrapper(
                simulations)

    def write_result(self, result):
        (raw_parameters, simulation_measurements,
            raw_filaments, filament_measurements) = result

        # Get or create parameter set group
        par_set_number, parameters = raw_parameters

        par_set_group = self.parameter_sets.select_child_number(
                par_set_number)


        # Write parameters if needed.
        if not len(par_set_group.parameters):
            par_set_group.parameters.write(parameters)

        # Time to start writing results.
        num_written_simulations = par_set_group.simulations._v_nchildren
        num_written_simulations = len(par_set_group.simulations)
        sim_group = par_set_group.sim_group.create_child_from_number(
                num_written_simulations)

        sim_group.measurements.write(simulation_measurements)

        for i, (fm, states) in enumerate(itertools.izip(filament_measurements,
                                                        raw_filaments)):
            fg = sim_group.filaments.create_child_from_number(i)
            fg.measurements.write(fm)
            fg.final_state.write(states)
