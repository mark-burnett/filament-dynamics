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

import kmc
import mp_sim

@baker.command
def depolymerization(configuration_filename,
                     output_filename='sim_results.pickle',
                     multiprocess=True):
    """
    Simulate a depolymerization timecourse.
    :param output_filename: Default: 'sim_results.pickle'
    """
    # Read configuration
    total_config = json.load(file(configuration_filename))
    config = total_config['depolymerization_simulation']

    # Construct simulation.
    sim = kmc.factories.build_depolymerization_simulation(
            total_config['model_type'], total_config['parameters'],
            config['polymerization_duration'],
            config['depolymerization_duration'],
            config['polymerization_concentrations'],
            config['barbed_end'], config['pointed_end'])

    # Construct initial_strand
    initial_strand = [config['initial_state'] for i in xrange(config['initial_size'])]

    # Run simulation
    if multiprocess:
        result = mp_sim.pool_sim(sim, initial_strand,
                                 num_simulations = config['num_simulations'],
                                 num_processes   = config['num_processes'])
    else:
        result = [sim(initial_strand)
                  for i in xrange(config['num_simulations'])]

#    # Reorganize results
#    depoly_results = zip(*result)[1]
#    length_profiles = [d['length'] for d in depoly_results]
#
#    # Write output
#    cPickle.dump({'simulation_type':'depolymerization',
#                  'length_profiles':length_profiles,
#                  'config':config,
#                  'timestamp':time.gmtime()},
#                 file(output_filename, 'w'), -1)
#
baker.run()
