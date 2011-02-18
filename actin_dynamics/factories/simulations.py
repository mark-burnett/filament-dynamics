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

from . import shortcuts

from ..simulations import Simulation

def make_run(run):
    parameters = run.all_parameters

    filaments      = binds.instantiate_binds(run.filaments, parameters)
    transitions    = binds.instantiate_binds(run.transitions, parameters)
    measurements   = binds.instantiate_binds(run.measurements, parameters)
    end_conditions = binds.instantiate_binds(run.end_conditions, parameters)
    concentrations = binds.instantiate_binds(run.concentrations, parameters)

    return Simulation(transitions=transitions, concentrations=concentrations,
                      measurements=measurements, end_conditions=end_conditions,
                      filaments=filaments)


# XXX Depracated
def make_simulation(object_graph, parameters):
    filaments = shortcuts.make_filaments(object_graph['filaments'],
                                         parameters)

    transitions = shortcuts.make_transitions(object_graph['transitions'],
                                             parameters)

    measurements = shortcuts.make_measurements(
            object_graph['measurements'], parameters)

    end_conditions = shortcuts.make_end_conditions(
            object_graph['end_conditions'], parameters)

    concentrations = shortcuts.make_concentrations(
            object_graph['concentrations'], parameters)

    return Simulation(transitions=transitions, concentrations=concentrations,
                      measurements=measurements, end_conditions=end_conditions,
                      filaments=filaments)


def simulation_generator(object_graph, parameters):
    try:
        # XXX Is this still where # of sims lives?
        number_simulations = parameters['number_of_simulations']
    except:
        print parameters
        raise

    for i in xrange(int(number_simulations)):
        yield make_simulation(object_graph, parameters)
