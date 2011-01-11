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


def _single_simulation_generator(object_graph, parameters, number_simulations):
    current_sim = 0
    while current_sim < number_simulations:
        yield make_simulation(object_graph, parameters)
        current_sim += 1

def simulation_generator(object_graph, parameters, number_simulations):
    for current_pars in parameters:
        yield current_pars, _single_simulation_generator(object_graph,
                                                         current_pars,
                                                         number_simulations)
