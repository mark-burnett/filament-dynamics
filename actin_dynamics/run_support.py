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

import cPickle as _cPickle

from . import io as _io
from . import simulations as _simulations

from .analysis.standard_error_of_mean import analyze_parameter_set

def typical_run(parameters, simulation_iterator):
    sim_results = map(run_and_report, simulation_iterator)
    full_set = {'parameters': parameters, 'simulations': sim_results}

    return analyze_parameter_set(full_set)


def run_simulations(simulation_factory, output_file_name):
    output_stream = _io.compressed.output_stream(output_file_name)
    for parameters, simulation_iterator in simulation_factory:
        analyzed_set = typical_run(parameters, simulation_iterator)

        _cPickle.dump(analyzed_set, output_stream,
                      protocol=_cPickle.HIGHEST_PROTOCOL)

    output_stream.close()


def run_and_report(sim):
    _simulations.run_simulation(sim)
    return report_measurements(sim)


def report_measurements(sim):
    concentration_results = {}
    for state, c in sim.concentrations.iteritems():
        concentration_results[state] = zip(*c.data)

    filament_results = []
    for filament in sim.filaments:
        fr = {}
        fr['final_state']  = filament.states
        fr['measurements'] = dict((name, zip(*values))
                for name, values in filament.measurements.iteritems())
        filament_results.append(fr)

    return {'concentrations': concentration_results,
            'filaments':      filament_results}
