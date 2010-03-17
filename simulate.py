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
import data_collectors
import mp_sim

@baker.command
def depolymerization(configuration_filename,
                     output_filename='sim_results.pickle',
                     model_type='vectorial',
                     barbed_end=True,
                     pointed_end=False):
    """
    Simulate a depolymerization timecourse.
    :param output_filename: Default: 'sim_results.pickle'
    :param model_type: Model to simulate. Allowed: 'vectorial'
    :param barbed_end: Boolean, simulate barbed end?
    :param pointed_end: Boolean, simulate pointed end?
    """
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

    # Construct polymerization and depolymerization rates.
    poly_rates, depoly_rates = construct_rates(config['parameters'], barbed_end, pointed_end)

    # Construct data collectors for depolymerization timecourse.
    depoly_dc = {'length':data_collectors.record_periodic(
                    data_collectors.strand_length,
                    config['length_sample_timesteps'])}

    # Construct simulation
    if 'vectorial' == model_type:
        sim = polymerization.vectorial.construct_depolymerization_simulation(
                poly_rates, depoly_rates,
                config['parameters'], # Contains hydrolysis parameters
                {}, # Polymerization data collectors (empty)
                depoly_dc,
                config['polymerization_timesteps'],
                config['depolymerization_timesteps'])
    else:
        raise NotImplementedError()

    # Construct initial_strand
    initial_strand = construct_initial_strand(config, model_type)

    # Run simulation
    result = mp_sim.pool_sim(combined_simulation, initial_strand,
                             num_simulations = config['num_simulations'],
                             num_processes   = config['num_processes'])

    # Reorganize results
    depoly_results = zip(*result)[1]
    length_profiles = [d['length'] for d in depoly_results]

    # Write output
    cPickle.dump({'simulation_type':'depolymerization',
                  'length_profiles':length_profiles,
                  'config':config,
                  'model_type':model_type,
                  'barbed_end':barbed_end,
                  'pointed_end':pointed_end,
                  'timestamp':time.gmtime()},
                 file(output_filename, 'w'), -1)

baker.run()
