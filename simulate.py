#!/usr/bin/env python
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

"""
    This is the main polymerization script.
"""

import baker
import json
import cPickle
import time

from collections import deque

import polymerization
import mp_sim

@baker.command
def depolymerization(configuration_filename,
                     output_filename='sim_results.dat',
                     model_type='vectorial',
                     barbed_end=True,
                     pointed_end=False):
# Read configuration
    config = json.load(file(configuration_filename))

    # Calculate some secondary parameters
    config['polymerization_timesteps'] = int(
            config['polymerization_duration']/config['dt'])
    config['true_polymerization_duration'] =\
            config['polymerization_timesteps'] * config['dt']

    config['depolymerization_timesteps'] = int(
            config['depolymerization_duration']/config['dt'])
    config['true_depolymerization_duration'] =\
            config['depolymerization_timesteps'] * config['dt']

    config['length_sample_timesteps'] = int(
            config['length_sample_period']/config['dt'])
    config['true_length_sample_period'] =\
            config['length_sample_timesteps'] * config['dt']

# Construct polymerization and depolymerization rates
    poly_rates, depoly_rates = construct_rates(config['parameters'], barbed_end, pointed_end)

# Construct initial_strand
    initial_strand = construct_initial_strand(config, model_type)

# Construct Simulation
    # Create polymerization simulation
        # Construct end conditions
    poly_ec = polymerization.end_conditions.Counter(
                config['polymerization_timesteps'])
    poly_sim = polymerization.Simulation(poly_rates, depoly_rates,
                                         hydro_object, {}, poly_ec)
    # Create depolymerization simulation
        # Construct data collectors
    depoly_dc = {'length':data_collectors.record_periodic(
                    data_collectors.strand_length,
                    config['length_sample_timesteps'])}
        # Construct hydrolysis handler
    hydrolysis = construct_hydrolysis_handler(config['parameters'], model_type)
        # Construct end conditions
    depoly_ec = polymerization.end_conditions.Counter(
                    config['depolymerization_timesteps'])
    depoly_sim = polymerization.Simulation(polymerization.simulation.NoOp,
                                           depoly_rates, hydro_object,
                                           depoly_dc, depoly_ec)

    # Combine simulations
    combined_simulation = polymerization.SimulationSequence([poly_sim,
                                                             depoly_sim])

# Run combined simulation
    result = mp_sim.pool_sim(combined_simulation, initial_strand,
                             num_simulations = config['num_simulations'],
                             num_processes   = config['num_processes'])

# Reorganize results
    depoly_results = zip(*result)[1]
    length_profiles = [d['length'] for d in depoly_results]
    # FIXME - make this make sense
    reorganized_lengths = statisticalize(length_profiles)

# Write output
    cPickle.dump({'simulation_type':'depolymerization',
                  'reorganized_lengths':reorganized_lengths,
                  'config':config,
                  'model_type':model_type,
                  'barbed_end':barbed_end,
                  'pointed_end':pointed_end,
                  'timestamp':time.gmtime()},
                 file(output_filename, 'w'), -1)

baker.run()
