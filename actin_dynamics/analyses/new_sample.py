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

import scipy.interpolate

from actin_dynamics.io.hdf.reader import MultipleSimulationReader

def downsample_simulation_measurement(hdf_file=None, name=None,
                                      sample_times=None):
    # Read in the simulation.
    simulations_group = hdf_file.getNode('/Simulations')
    reader = MultipleSimulationReader(simulations_group)
    data = reader.collect_simulation_measurements(name)

    # Perform downsampling.
    downsampled_data = []
    for d in data:
        downsampled_data.append(resample(d, sample_times))

    # Write that shiz.
    # XXX hm
    writer = AnalysisWriter(output_group)
    writer.write(downsampled_data)

def resample(data, sample_times):
    times, values = zip(data)
    if len(values) < 2:
        return [values[0] for t in sample_times]
    interp = scipy.interpolate.interp1d(times, values,
                                        copy=False, bounds_error=False,
                                        fill_value=data[-1])
    return interp(sample_times)
