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

from . import interpolation

from actin_dynamics.io import hdf as _hdf

def all_measurements(parameter_sets_wrapper, analysis_wrapper,
                     sample_period=1, epsilon=1e-10):
    for parameter_set in parameter_sets_wrapper:
        sample_times = numpy.arange(0,
                parameter_set.parameters['simulation_duration'] + epsilon,
                sample_period)

        analysis_ps = analysis_wrapper.create_child(parameter_set.name)

        for simulation in parameter_set.simulations:
            # calculate simulation measurements
            sm_results = collection_measurements(
                    simulation.simulation_measurements, sample_times)

            sa_wrapper = analysis_ps.simulations.create_child(simulation.name)

            # write simulation measurements
            sa_wrapper.write_measurements(sm_results)

            sa_filaments = sa_wrapper.filaments
            for filament in simulation.filaments:
                # calculate filament measurements
                fm_results = collection_measurements(filament.measurements,
                                                     sample_times)

                # simulation result wrapper
                filament_analysis_wrapper = sa_filaments.create_child(
                        filament.name)

                # write filament measurements
                filament_analysis_wrapper.measurements.write(fm_results)


def collection_measurements(measurements, sample_times):
    results = {}
    # XXX make simulation.measurements.iteritems()
    for m in measurements:
        results[m.name] = zip(*interpolation.resample_measurement(
                zip(*m.read()), sample_times, method='previous_value'))
    return results
