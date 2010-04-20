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

import collections

import polymerization.factories   as pf
import depolymerization.factories as df
import hydrolysis.factories       as hf

import end_conditions
import data_collectors

import simulation

__all__ = ['initial_strand', 'simulation']

# Initial strand
# ----------------------------------------------------------------------
def initial_strand(simulation_config, model_config):
    type = list
    if simulation_config['pointed_end']:
        type = collections.deque
    return type(model_config['seed_states'][simulation_config['seed_state']]
                for i in xrange(simulation_config['initial_size']))

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

def single_sim(model_config, stage, free_barbed_end, free_pointed_end):
    # End conditions
    ecs = []
    for end_signature in stage['end_conditions']:
        ecs.append(single_end_condition(end_signature))
    if not ecs:
        raise RuntimeError('No end conditions specified.')

    # Polymerization transitions
    poly_config = None
    try:
        poly_config =  stage['polymerization']
    except KeyError:
        pass

    if poly_config:
        poly = pf.normal(model_config['parameters'], poly_config,
                         free_barbed_end, free_pointed_end)
    else:
        poly = []

    # Depolymerization transitions
    depoly = df.normal(model_config['parameters'],
                       free_barbed_end, free_pointed_end)

    # Hydrolysis transitions
    hydro = hf.constant_rates(model_config['model_type'],
                              model_config['parameters']['hydrolysis_rates'],
                              free_barbed_end, free_pointed_end)

    # Data collectors
    dcs = {}
    for collector_signature in stage['data_collectors']:
        dcs[collector_signature] = single_data_collector(collector_signature)

    return simulation.Simulation(poly + depoly + hydro, ecs, dcs)

# End Conditions
# ----------------------------------------------------------------------
def _ec_duration(duration):
    return end_conditions.MaxVariable('sim_time', duration)

def _ec_random_duration(max_duration):
    return end_conditions.RandomMaxVariable('sim_time', max_duration)

_ec_signatures = {'duration':        _ec_duration,
                  'random_duration': _ec_random_duration}

def single_end_condition(signature):
    return _ec_signatures[signature[0]](*signature[1:])

# Data Collectors
# ----------------------------------------------------------------------
def _dc_simulation_time():
    return data_collectors.Variable('sim_time')

def _dc_strand_length():
    return data_collectors.strand_length

def _dc_cleavage_event():
    return data_collectors.HydrolysisEventCounter('t', 'p')

def _dc_release_event():
    return data_collectors.HydrolysisEventCounter('p', ['d', 'du', 'ds'])

_dc_signatures = {'simulation_time': _dc_simulation_time,
                  'strand_length':   _dc_strand_length,
                  'cleavage_events': _dc_cleavage_event,
                  'release_events':  _dc_release_event}

def single_data_collector(signature):
    return _dc_signatures[signature]()
