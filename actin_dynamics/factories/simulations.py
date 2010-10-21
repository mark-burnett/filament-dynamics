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

import random

from . import shortcuts

from ..simulations import Simulation

def make_simulation(object_graph, parameters):
    filaments = shortcuts.make_filaments(object_graph['filaments'],
                                         parameters)
    print 'num fil', len(filaments)

    transitions = shortcuts.make_transitions(object_graph['transitions'],
                                             parameters)
    print transitions

    # XXX create explicit measurements?

    end_conditions = shortcuts.make_end_conditions(
            object_graph['end_conditions'], parameters)
    print end_conditions

    concentrations = shortcuts.make_concentrations(
        object_graph['concentrations'], parameters)

    # assemble simulation
    return Simulation(transitions, concentrations, explicit_measurements,
                      end_conditions, strand_factory, random.uniform)

class SimulationFactory(object):
    def __init__(self, object_graph, parameters):
        self.object_graph = object_graph
        self.parameters = parameters

    def __iter__(self):
        return self

    def next(self):
        return make_simulation(self.object_graph, next(self.parameters))
