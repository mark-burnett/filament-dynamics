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
    This is the main simulation script.
"""

import time
import operator
import os

import json
import cPickle

import baker

import hydro_sim
import util.mp_sim

@baker.command(default=True)
def hydrolysis(model_file, simulation_file,
               N=100, processes=0,
               output_file=None,
               output_dir=None):
    """
    Perform hydrolysis simulation (default).
    :param output_file: Filename for storing results.
    :param processors:  Number of processors to use (default=autodetect).
    :param N:           Number of simulations to run (default=100).
    """
    # Read model and simulation config files
    model_config      = json.load(open(model_file))
    simulation_config = json.load(open(simulation_file))

    # Construct simulation
    sim_generator = hydro_sim.factories.full_simulation_generator(model_config,
            simulation_config)

    # Construct initial strand
    initial_strand_config = simulation_config['initial_strand']
    strand_generator = hydro_sim.strand.factory(initial_strand_config,
                                                model_config)

    # Run simulation
    if 1 == processes:
        sims, data = zip(itertools.islice(sim_generator, N))
        strands    = itertools.islice(strand_generator, N)
        [sim(strand) for sim, strand in itertools.izip(sims, strands)]
    else:
        sims, data = zip(itertools.islice(sim_generator, N))
        strands    = itertools.islice(strand_generator, N)
        util.mp.multi_map(sims, strands, processes)

    # Construct output filename
    if output_file:
        filename = output_file
    else:
        filename = '_'.join([model_config['filename'], simulation['filename'],
                            str(N)]) + '.pickle'
    
    if output_dir:
        # Create output directory
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # Adjust output path
        filename = os.path.join(output_dir, filename)

    # Write output
    with open(filename, 'w') as f:
        cPickle.dump({'model_config': model_config,
                      'simulation_config': simulation_config,
                      'data': data,
                      'timestamp':time.gmtime()},
                     f, -1)

baker.run()
