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

import itertools
import collections

import util

import kmc.end_conditions
import kmc.generators

import hydro_sim.concentrations
import hydro_sim.transitions
import hydro_sim.measurements
import hydro_sim.strand

__all__ = ['full_simulation_generator']

def make_simulation(model_config, simulation_config):
    stages = [make_stage(model_config, stage_config)
              for stage_config in simulation_config['stages']]

    return kmc.generators.sequence(stages)

def make_stage(model_config, stage_config):
    concentrations = make_concentrations(model_config['states'],
                                         stage_config['concentrations'])
    return kmc.generators.simulation(
            make_transitions(model_config['transitions'],
                             concentrations),
            make_end_conditions(stage_config['end_conditions']),
            make_measurements(stage_config['measurements']))

def make_concentrations(model_states, concentrations_config):
    conc_dict = {}
    if concentrations_config:
        config_states, config_functions = zip(*concentrations_config)
        states = [util.states.match(model_states, cs) for cs in config_states]
        factories = util.introspection.make_factories(config_functions,
                                                      hydro_sim.concentrations)
        conc_dict = dict((state, f(*args))
                         for state, (f, args) in zip(states, factories))
    return collections.defaultdict(hydro_sim.concentrations.zero_concentration,
                                   conc_dict)

def make_transitions(transitions_config, concentrations):
    factories = util.introspection.make_factories(transitions_config,
                                                  hydro_sim.transitions)
    return [f(concentrations, *args) for f, args in factories]

def make_end_conditions(ec_config):
    ec_factories = util.introspection.make_factories(ec_config,
                                                     kmc.end_conditions)
    return [f(*args) for f, args in ec_factories]

def make_measurements(measurements_config):
    return [util.introspection.lookup_name(name,
                hydro_sim.measurements)(label, *args)
            for label, (name, args) in measurements_config.items()]

def make_strand(initial_strand_config, model_config):
    name, args = initial_strand_config
    f = util.introspection.lookup_name(name, hydro_sim.strand)
    return f(model_config['states'], *args)
