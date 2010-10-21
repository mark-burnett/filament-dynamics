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

from . import utils

from . import shortcuts
from .concentrations import make_concentrations

from ..simulations import Simulation

from actin_dynamics.common import logutils
logger = logutils.getLogger(__file__)

__all__ = ['make_simulation']

def make_simulation(simulation, parameter_set):
    logger.debug('Instantiating Simulation: simulation=%s, parameter_set=%s.'
                 % (simulation, parameter_set))
    # create parameter map (dict)
    parameter_value_map = utils.make_parameter_value_map(parameter_set)

    # create initial strand
    strand_factory = shortcuts.make_strand_factory(parameter_value_map,
            simulation.strand_factory_binding)

    # create transitions
    transitions = utils.make_many(shortcuts.make_transition,
                                  parameter_value_map,
                                  simulation.transitions)

    # create explicit measurements
    explicit_measurements = utils.make_many(shortcuts.make_explicit_measurement,
                                            parameter_value_map,
                                            simulation.explicit_measurements)

    # create end conditions
    end_conditions = utils.make_many(shortcuts.make_end_condition,
                                     parameter_value_map,
                                     simulation.end_conditions)

    # create concentrations
    concentrations =  make_concentrations(parameter_value_map,
                                          simulation.concentrations)

    # assemble simulation
    return Simulation(transitions, concentrations, explicit_measurements,
                      end_conditions, strand_factory, random.uniform)

class SimulationFactory(object):
    def __init__(self, object_graph, parameter_iterator):
        self.object_graph = object_graph
        self.parameter_iterator = parameter_iterator

    def __iter__(self):
        return self

    def next(self):
        return make_something_happen(self.object_graph, next(self.parameters))
