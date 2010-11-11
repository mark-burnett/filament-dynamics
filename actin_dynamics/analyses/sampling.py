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

import collections

import numpy
import scipy.interpolate

import tables

class DownsampledMeasurement(tables.IsDescription):
    value = tables.FloatCol()

def downsample(hdf_file, sample_period, duration_name='simulation_duration'):
    simulations = hdf_file.getNode('/Simulations')
    analysis_group = hdf_file.getNode('/Analysis')
    try:
        output_group = hdf_file.createGroup(analysis_group, 'sampled_data',
                                            'Downsampled data.')
    except tables.NodeError:
        # Node exists, no problem.
        output_group = analysis_group.sampled_data

    # XXX set sample period metadata in output group

    for simulation in simulations:
        duration = _get_parameter(simulation.parameters, duration_name)
        sample_times = numpy.arange(0, duration, sample_period)

        # Simulation measurements
        try:
            sm_group = hdf_file.createGroup(output_group,
                                            'simulation_measurements')
        except tables.NodeError:
            # Node exists, no problem.
            sm_group = output_group.simulation_measurements

        _downsample_group(simulation.simulation_measurements, hdf_file,
                          sm_group, sample_times)

        try:
            filaments_out_group = hdf_file.createGroup(output_group, 'filaments')
        except tables.NodeError:
            filaments_out_group = output_group.filaments

        # Filament measurements - don't duplicate e.g. final state.
        for f in simulation.filaments:
            try:
                filament_group = hdf_file.createGroup(filaments_out_group, f._v_name)
            except tables.NodeError:
                filament_group = output_group._f_getChild(f._v_name)
            _downsample_group(f, hdf_file, filament_group, sample_times)

def _get_parameter(parameters, name):
    for p in parameters:
        if name == p['name']:
            return p['value']

def _downsample_group(data_group, hdf_file, output_group, sample_times):
    for node in data_group:
        # Skip non-measurements.
        if 'final_states' == node._v_name:
            continue

        downsampled_measurement = _get_downsampled_table(node, sample_times)

        try:
            table = hdf_file.createTable(output_group, node._v_name,
                                         DownsampledMeasurement)
        except tables.NodeError:
            table = output_group._f_getChild(node._v_name)

        for m in downsampled_measurement:
            table.row['value'] = m
            table.row.append()

        table.flush()

def _get_downsampled_table(source_table, sample_times):
    results = _table_to_dict(source_table)
    return _downsample(results['time'], results['value'], sample_times)

def _table_to_dict(table):
    dd = collections.defaultdict(list)
    for row in table:
        for name in table.colnames:
            dd[name].append(row[name])
    return dd

def _downsample(times, measurements, new_times):
    interp = scipy.interpolate.interp1d(times,
                                        measurements,
                                        copy=False,
                                        bounds_error=False,
                                        fill_value=measurements[-1])
    return interp(new_times)
