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

import numpy
import scipy.interpolate

from actin_dynamics.io import hdf as _hdf

def all_measurements(parameter_sets_wrapper, analysis_wrapper,
                     sample_period=1):
    for parameter_set in parameter_sets_wrapper:
        sample_times = numpy.arange(0, parameter_set['simulation_duration'],
                                    sample_period)
        analysis_ps = analysis_wrapper.create_child(parameter_set.name)

        for simulation in parameter_set:
            print 'begin', simulation.name
            # calculate simulation measurements
            sm_results = collection_measurements(simulation, sample_times)

            simulation_analysis_wrapper = analysis_ps.create_subgroup(
                    name=simulation.name,
                    wrapper=_hdf.SimulationWrapper)

            # write simulation measurements
            simulation_analysis_wrapper.write_measurements(sm_results)

            sa_filaments = simulation_analysis_wrapper.filaments
            for filament in simulation.filaments:
                # calculate filament measurements
                fm_results = collection_measurements(filament, sample_times)

                # simulation result wrapper
                filament_analysis_wrapper = sa_filaments.create_child(
                        filament.name)

                # write filament measurements
                filament_analysis_wrapper.measurements.write(fm_results)

            print 'end', simulation.name


def collection_measurements(simulation, sample_times):
    results = {}
    # XXX make simulation.measurements.iteritems()
    for m in simulation.measurements:
        results[m.name] = resample(m.read(), sample_times)
    return results


# This is the only function in this file that does actual work.
def resample(data, sample_times):
    '''
    Downsample data to sample_times.

    For now this is linear interpolation, but later it might need to become
    a previous-value interpolation.
    '''
    times, values = zip(*data)
    if len(values) < 2:
        return [(t, values[0]) for t in sample_times]
    interp = scipy.interpolate.interp1d(times, values,
                                        copy=False, bounds_error=False,
                                        fill_value=values[-1])
    return zip(sample_times, interp(sample_times))
