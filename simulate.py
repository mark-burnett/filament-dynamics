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
import itertools

import json
import cPickle

import baker

import hydro_sim
import util.mp_sim

@baker.command(default=True)
def hydrolysis(model_template,      model_parameters,
               experiment_template, experiment_parameters,
               N=100, processes=0,
               output_file=None,
               output_dir=None):
    """
    Perform hydrolysis simulation (default).
    :param output_file: Filename for storing results.
    :param processors:  Number of processors to use (default=autodetect).
    :param N:           Number of simulations to run (default=100).
    """
    try:
        # Read template files -> strings.
        pass
    except:
        # Print valid template names.
        raise RuntimeError('Invalid template name.  Valid names are: %s.')

    # Read parameter files.

    # Complete templates.

    # Read model and simulation config files
#    model_config      = json.load(open(model_file))
#    simulation_config = json.load(open(simulation_file))

    # Construct simulation
    sim_generator = hydro_sim.factories.simulation_generator(model_config,
                                                             simulation_config)

    # Construct initial strand
    strand_generator = hydro_sim.factories.make_sequence_generator(
                           simulation_config['initial_strand'],
                           model_config['states'])

    # Run simulation
    if 1 == processes:
        data = [sim(strand)
                for sim, strand in itertools.islice(
                    itertools.izip(sim_generator, strand_generator), N)]
    else:
        data = util.mp_sim.multi_map(itertools.islice(sim_generator, N),
                                     strand_generator, processes)

    # Construct output filename
    if output_file:
        filename = output_file
    else:
        filename = '_'.join([model_config['filename'],
                             simulation_config['filename'],
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
