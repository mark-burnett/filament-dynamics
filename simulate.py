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

import json
import cPickle

import baker

import hydro_sim
import mp_sim

@baker.command(default=True)
def hydrolysis(model_file, simulation_file,
               N=100, processors=None,
               output_file=None):
    """
    Perform hydrolysis simulation (default).
    :param output_file: Filename for storing results.
    :param processors:  Number of processors to use (default=autodetect).
    :param N:           Number of simulations to run (default=100).
    """
    # Read model and simulation config files
    model_config      = json.load(file(model_file))
    simulation_config = json.load(file(simulation_file))

    # Construct simulation
    sim = hydro_sim.factories.build_simulation(model_config, simulation_config)

    # Construct initial strand
    initial_strand = hydro_sim.factories.initial_strand(simulation_config)

    # Run simulation
    if 1 == processors:
        data = [sim(initial_strand) for i in xrange(N)]
    else:
        data = mp_sim.pool_sim(sim, initial_strand, N, processors)

    # Write output
    if output_file:
        filename = output_file
    else:
        raise NotImplementedError('Figure out output filename.')

    with file(filename, 'w') as f:
        cPickle.dump({'model_config': model_config,
                      'simulation_config': simulation_config,
                      'data': data,
                      'timestamp':time.gmtime()},
                     f, -1)

baker.run()
