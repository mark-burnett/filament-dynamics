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

    transitions = shortcuts.make_transitions(object_graph['transitions'],
                                             parameters)

    measurements = shortcuts.make_measurements(
            object_graph['measurements'], parameters)

    end_conditions = shortcuts.make_end_conditions(
            object_graph['end_conditions'], parameters)

    concentrations = shortcuts.make_concentrations(
        object_graph['concentrations'], parameters)

    return Simulation(transitions, concentrations, measurements,
                      end_conditions, filaments, random.uniform)

class SimulationFactory(object):
    def __init__(self, object_graph, parameters):
        self.object_graph = object_graph
        self.parameters = parameters

    def __iter__(self):
        return self

    def next(self):
        return make_simulation(self.object_graph, next(self.parameters))
