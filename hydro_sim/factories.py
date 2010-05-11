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

import copy
import itertools
import collections

import util

import kmc.end_conditions
import kmc.simulation

from . import simulation

from . import concentrations
from . import transitions
from . import measurements
from . import strand

def simulation_generator(model_config, simulation_config):
    sim = make_simulation(model_config, simulation_config)
    while True:
        yield copy.deepcopy(sim)

def make_simulation(model_config, simulation_config):
    model_states = model_config['states']
    concentrations = []
    stages = []
    for stage_config in simulation_config['stages']:
        stages.append(make_stage(model_config, stage_config))
        concentrations.append(make_concentrations(model_states,
                                              stage_config['concentrations']))

    return simulation.SimulationSequence(model_states, stages, concentrations)

def make_stage(model_config, stage_config):
    return kmc.simulation.Simulation(
            make_transitions(model_config['transitions']),
            make_measurements(stage_config['measurements']),
            make_end_conditions(stage_config['end_conditions']))

def make_concentrations(model_states, concentrations_config):
    conc_dict = {}
    for config_states, (config_function, config_args) in concentrations_config:
        state = util.states.match(model_states, config_states)
        f = util.introspection.lookup_name(config_function, concentrations)
        conc_dict[state] = f(*config_args)
    return collections.defaultdict(concentrations.zero_concentration,
                                   conc_dict)

def make_transitions(transitions_config):
    factories = util.introspection.make_factories(transitions_config,
                                                  transitions)
    return [f(*args) for f, args in factories]

def make_end_conditions(ec_config):
    ec_factories = util.introspection.make_factories(ec_config,
                                                     kmc.end_conditions)
    return [f(*args) for f, args in ec_factories]

def make_measurements(measurements_config):
    return [util.introspection.lookup_name(name,
                measurements)(label, *args)
            for label, (name, args) in measurements_config.items()]

def make_sequence_generator(initial_strand_config, model_states):
    name, args = initial_strand_config
    f = util.introspection.lookup_name(name, strand)
    return f(model_states, *args)
