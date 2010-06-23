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

import baker

import json
import csv

from mako.template import Template

@baker.command
def surface(model_template_name, fit_parameters_filename,
            experiment_template_name, experiment_parameters_filename,
            N=6, processes=0,
            parameter_mesh_size=100,
            output_dir='',
            output_file='',
            template_dir='templates',
            template_extension='.template'):
    # Load model template
    model_template = Template(filename=os.path.join(template_dir, 'models',
                              model_template_name + template_extension))
    # Load fit parameters
    fit_parameters = json.load(open(fit_parameters_filename))

    # Create example model config so we can get model states.
    example_model_parameters = fit_parameters['fixed']
    for par_name, (low_value, high_value) in fit_parameters['variable']:
        example_model_parameters[par_name] = low_value
    example_model_config = json.loads(model_template.render(
        **make_kwargs_ascii(example_model_parameters)))
    model_states = example_model_config['states']

    # Populate experiment parameters
    experiment_parameters = json.load(open(experiment_parameters_filename))
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

    strand_generator = hydro_sim.factories.make_sequence_generator(
                           model_states,
                           experiment_config['initial_strand'])

    # Create parameter meshes
    parameter_meshes = {}
    for par_name, (low_value, high_value) in fit_parameters['variable']:
        parameter_meshes[par_name] = make_parameter_mesh(low_value, high_value,
                                                         parameter_mesh_size)

    # XXX Load data

    # Base model parameters
    base_model_parameters = fit_parameters['fixed']
    # Loop over variable parameteres
    for par_names, par_values in something:
        # Generate model config
        model_parameters = copy.copy(base_model_parameters)
        for pn, pv in itertools.izip(par_names, par_values):
            model_parameters[pn] = pv
        model_config = json.loads(model_template.render(
            **make_kwargs_ascii(model_parameters)))

        # Build simulation
        # Construct simulation generators.
        sim_generator = hydro_sim.factories.simulation_generator(
                                                      model_config,
                                                      stage_configs)
        # Run simulations.
        if 1 == processes:
            data = [sim(strand)
                    for sim, strand in itertools.islice(
                        itertools.izip(sim_generator, strand_generator), N)]
        else:
            data = util.mp_sim.multi_map(itertools.islice(sim_generator, N),
                                         strand_generator, processes)

        # Perform analysis
        cleavage_data = [d['phosphate_cleavage'] for d in data]
        sampled_data = analysis.sampling.downsample_each(experiment_times, cleavage_data)
        cleavage_avg, cleavage_std = analysis.statistics.avg_std(cleavage_data)

        # Calculate residual
        # add simulation variance to experiment variance
        residual_std = numpy.sqrt(cleavage_std**2 + experiment_std**2)
        residual = fitpy.algorithms.utils.residuals.chi_squared(
                experiment_times, experiment_data, residual_std, cleavage_avg)
        results.append([pv for pv in par_values] + [residual])

    # Write csv file

#
#@baker.command
#def fit(model_template_name,
#        fit_parameters_file,
#        experiment_template_name,
#        experiment_parameters_filename):
#    pass
