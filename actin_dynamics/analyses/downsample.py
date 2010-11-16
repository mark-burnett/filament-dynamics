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

def all_measurements(parameter_sets_wrapper, analysis_wrapper,
                     sample_period=1):
    for parameter_set in parameter_sets_wrapper:
        sample_times = numpy.arange(0, parameter_set['simulation_duration'], sample_period)

        for simulation in parameter_set:
            # calculate simulation measurements
            sm_results = simulation_measurements(simulation, sample_times)

            simulation_analysis_wrapper = SimulationAnalysisWrapper.for_analysis(analysis_wrapper)

            # write simulation measurements
            simulation_analysis_wrapper.write_analyses(sm_results)

            for filament in simulation:
                # calculate filament measurements
                fm_results = filament_measurements(filament, sample_times)

                # simulation result wrapper
                filament_analysis_wrapper = FilamentAnalysisWrapper.for_analysis(
                        simulation_analysis_wrapper)
                # write filament measurements
                filament_analysis_wrapper.write_analyses(fm_results)


def resample(data, sample_times):
    times, values = zip(data)
    if len(values) < 2:
        return [values[0] for t in sample_times]
    interp = scipy.interpolate.interp1d(times, values,
                                        copy=False, bounds_error=False,
                                        fill_value=data[-1])
    return interp(sample_times)
