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
import util

import kmc.end_conditions
import kmc.generators

import hydro_sim.concentrations
import hydro_sim.transitions
import hydro_sim.data_collectors

__all__ = ['full_simulation_generator']

def single_generator_factory(model_states,
                             conc_config, trans_config,
                             dc_config, ec_config):
    conc_fac  = concentrations_factory(model_states, conc_config)
    trans_fac = transitions_factory(trans_config, conc_fac)
    dc_fac    = data_collectors_factory(dc_config)
    ec_fac    = end_conditions_factory(ec_config)
    return kmc.generators.simulation(trans_fac, ec_fac, dc_fac)

def full_simulation_generator(model_config, simulation_config):
    # Build generators for each stage.
    model_states = model_config['states']
    trans_config = model_config['transitions']
    sim_gen = [single_generator_factory(model_states,
                   stage['concentrations'], trans_config,
                   stage['data_collectors'], stage['end_conditions'])
               for stage in simulation_config['stages']]

    while True:
        # Make list of stage simulations and repositories
        sims, data_repository = zip([sg.next() for sg in sim_gen])
        yield util.compose(s.run for s in sims), data_repository

def concentrations_factory(model_states, concentration_config):
    config_states, config_functions = zip(concentration_config)
    states    = [util.states.find_matching(model_states, cs)
                 for cs in config_states]
    factories = util.introspection.make_factories(config_functions,
                                                  hydro_sim.concentrations)

    def make_cs(pub):
        return dict((state, f(pub, *args))
                    for state, (f, args) in itertools.izip(states, factories))
    return make_cs

def transitions_factory(config_transitions, concentrations_factory):
    factories = util.introspection.make_factories(config_transitions,
                                                  hydro_sim.transitions)

    def make_ts(pub):
        # construct conditions/concentrations
        concentrations = concentrations_factory(pub)

        # construct transitions
        return [f(pub, concentrations, *args)
               for f, args in transition_factories]
    return make_ts

def data_collectors_factory(dc_config):
    # This is the stuff that gets reused.
    dc_names = [name for name, junk in dc_config]
    dc_factories = util.introspection.make_factories(dc_config,
                                                     hydro_sim.data_collectors)

    def make_dcs(pub):
        # Create repository for data.
        data_repositories = dict((name, []) for name in dc_names)
        # Setup data collectors on that repository.
        data_collectors   = [f(pub, dr[name], *args)
                             for name, dr, (f, args) in itertools.izip(
                                 dc_names, data_repositories, dc_factories)]
        return data_repositories
    return make_dcs

def end_conditions_factory(ec_config):
    ec_factories = util.introspection.make_factories(ec_config,
                                                     kmc.end_conditions)
    def make_ecs(pub):
        return [f(pub, *args) for f in ec_factories]
    return make_ecs

# Simulations
# ----------------------------------------------------------------------
def build_simulation(model_config, simulation_config):
    # Loop over stages in order and build them.
    simulations = []
    for stage_name in simulation_config['stage_sequence']:
        stage = simulation_config['stages'][stage_name]
        sim = single_sim(model_config, stage,
                         simulation_config['barbed_end'],
                         simulation_config['pointed_end'])
        simulations.append(sim)

    # Always use a simulation sequence, even for just one stage.
    return simulation.SimulationSequence(simulations)
