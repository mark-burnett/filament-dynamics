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

from mako.template import Template
import baker

import hydro_sim
import util

@baker.command(default=True)
def hydrolysis(model_template_name,      model_parameters_filename,
               experiment_template_name, experiment_parameters_filename,
               N=100, processes=0,
               output_file=None,
               output_dir=None,
               template_dir='templates',
               template_extension='.template'):
    """
    Perform hydrolysis simulation (default).
    :param output_file:  Filename for storing results.
    :param processors:   Number of processors to use (default=autodetect).
    :param N:            Number of simulations to run (default=100).
    :param template_dir: Location of templates to use.
    :param template_extension: Filename extension for tempalte files (default='.template').
    """
    # Read parameter files.
    model_parameters      = json.load(open(model_parameters_filename))
    experiment_parameters = json.load(open(experiment_parameters_filename))

    # Load configuration dictionaries.
    model_config = util.config.get_model_config(model_parameters,
                                                model_template_name,
                                                template_dir,
                                                template_extension)
    model_states = model_config['states']

    experiment_config = util.config.get_experiment_config(
                                                  model_states,
                                                  experiment_parameters,
                                                  experiment_template_name,
                                                  template_dir,
                                                  template_extension)

    stage_configs = util.config.get_stage_configs(model_states,
                                                  experiment_config,
                                                  experiment_parameters,
                                                  template_dir,
                                                  template_extension)

    # Construct simulation generators.
    sim_generator = hydro_sim.factories.simulation_generator(
                                                  model_config,
                                                  experiment_config['stages'],
                                                  stage_configs)

    strand_generator = hydro_sim.factories.make_sequence_generator(
                           experiment_config['initial_strand'])

    # Run simulations.
    if 1 == processes:
        data = [sim(strand)
                for sim, strand in itertools.islice(
                    itertools.izip(sim_generator, strand_generator), N)]
    else:
        data = util.mp_sim.multi_map(itertools.islice(sim_generator, N),
                                     strand_generator, processes)

    # Construct output filename.
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
                      'experiment_config': experiment_config,
                      'stage_configs': stage_configs,
                      'model_parameters': model_parameters,
                      'experiment_parameters': experiment_parameters,
                      'data': data,
                      'timestamp':time.gmtime()},
                     f, -1)

baker.run()
