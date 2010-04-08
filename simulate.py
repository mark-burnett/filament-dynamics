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

import operator
import baker
import json
import cPickle
import time

import polymerization
import mp_sim

def run_sim(sim, initial_strand, multiprocess,
            output_file, simulation_type,
            total_config, config):
    # Run simulation
    if multiprocess:
        result = mp_sim.pool_sim(sim, initial_strand,
                                 num_simulations = config['num_simulations'],
                                 num_processes   = config['num_processes'])
    else:
        result = [sim(initial_strand)
                  for i in xrange(config['num_simulations'])]

    # Write output
    cPickle.dump({'simulation_type':simulation_type,
#                  'results':map(operator.itemgetter(1), result),
                  'results':result,
                  'config':total_config,
                  'timestamp':time.gmtime()},
                 output_file, -1)


@baker.command
def depolymerization(configuration_filename,
                     output_filename='depolymerization_results.pickle',
                     multiprocess=True):
    """
    Simulate a depolymerization timecourse.
    :param output_filename: Default: 'sim_results.pickle'
    :param multiprocess: Whether to use multiple cores.
    """
    # Read configuration
    total_config = json.load(file(configuration_filename))
    config = total_config['depolymerization_simulation']

    # Construct simulation.
    sim = polymerization.factories.build_depolymerization_simulation(
            total_config['model_type'], total_config['parameters'],
            config['polymerization_duration'],
            config['depolymerization_duration'],
            config['polymerization_concentrations'],
            config['barbed_end'], config['pointed_end'])

    # Construct initial_strand
    initial_strand = polymerization.factories.build_initial_strand(
            config['initial_size'], config['initial_state'],
            config['barbed_end'], config['pointed_end'])

    # Run simulation
    run_sim(sim, initial_strand, multiprocess,
            file(output_filename, 'w'), 'depolymerization',
            total_config, config)

@baker.command
def cleavage(configuration_filename,
             output_filename='cleavage_results.pickle',
             multiprocess=True):
    # Read configuration
    total_config = json.load(file(configuration_filename))
    config = total_config['cleavage_simulation']

    # Construct simulation.
    sim = polymerization.factories.build_cleavage_simulation(
            total_config['model_type'], total_config['parameters'],
            config['duration'], config['transition_from'],
            config['monomer_concentrations'],
            config['filament_tip_concentration'],
            config['barbed_end'], config['pointed_end'])

    # Construct initial_strand
    initial_strand = polymerization.factories.build_initial_strand(
            config['initial_size'], config['initial_state'],
            config['barbed_end'], config['pointed_end'])

    # Run simulation
    run_sim(sim, initial_strand, multiprocess,
            file(output_filename, 'w'), 'cleavage_polymerization',
            total_config, config)

baker.run()
