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

from . import wrappers as _wrappers

# XXX Consider making this writer a context?
class SimulationWriter(object):
    def __init__(self, hdf_file=None):
        self.hdf_file = hdf_file
        self.simulations = self.hdf_file.createGroup('/', 'Simulations',
                                                     'Raw Simulation Data')

    def write_result(self, result):
        (raw_parameters, simulation_measurements,
            raw_filaments, filament_measurements) = result

        # Get or create parameter set group
        par_set_number, parameters = raw_parameters
        par_set_group = _create_parameter_set_group(self.hdf_file,
                self.simulations, par_set_number)

        # Write parameters if needed.
        _write_parameters(self.hdf_file, par_set_group, parameters)

        # Time to start writing results.
        num_written_simulations = par_set_group.simulations._v_nchildren
        result_group = self.hdf_file.createGroup(par_set_group.simulations,
                                                 ('simulation_%s' %
                                                  num_written_simulations))

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
                    hdf_file=self.hdf_file, parent_group=fg,
                    name='measurements')
            fil_col.write(fm)

            state = _wrappers.State.in_group(hdf_file=self.hdf_file,
                    parent_group=fg, name='final_state')
            state.write(states)

def _create_parameter_set_group(hdf_file, parent_group, par_set_number):
    psg = getattr(parent_group, ('parameter_set_%s' % par_set_number), None)
    if psg is None:
        psg = hdf_file.createGroup(parent_group,
                                   'parameter_set_%s' % par_set_number)
        hdf_file.createGroup(psg, 'simulations')
    return psg

def _write_parameters(hdf_file, par_set_group, parameters):
    # XXX check for existing table first
    if getattr(par_set_group, 'parameters', None) is None:
        par_table = _wrappers.Parameters.in_group(hdf_file=hdf_file,
                                                  parent_group=par_set_group,
                                                  name='parameters')
        par_table.write(parameters)

class AnalysisWriter(object):
    def __init__(self, hdf_file=None, parent_group=None):
        self.hdf_file = hdf_file
        self.parent_group = parent_group

    def write_simulation_analysis(self, analysis_name=None, data=None):
        pass

    def write_filament_analysis(self, analysis_name=None, data=None):
        pass

    def write_summary_analysis(self, analysis_name=None, data=None):
        pass
