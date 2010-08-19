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
import os

import itertools
import copy

from mako.template import Template

import numpy

import hydro_sim.factories

import util.config
import util.mp_sim
from util.introspection import make_kwargs_ascii

import analysis.sampling
import analysis.statistics

from fitpy.utils import meshes
import fitpy.algorithms.common.residuals

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
    for par_name, (low_value, high_value) in fit_parameters['variable'].items():
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
    for par_name, (low_value, high_value) in fit_parameters['variable'].iteritems():
        parameter_meshes[par_name] = meshes.logmesh(low_value, high_value,
                                                    parameter_mesh_size)

    # XXX Load data
    experiment_times = []
    experiment_data = []
    experiment_std = []

    with open('data/experiments/pollard_cleavage.dat') as f:
        for et, ed, lower_bound, upper_bound in csv.reader(f, delimiter=' ', skipinitialspace=True):
            experiment_times.append(float(et))
            experiment_data.append(float(ed))

            std = (float(upper_bound) - float(lower_bound)) / 2
            experiment_std.append(std)

    experiment_times = numpy.array(experiment_times)
    experiment_data = numpy.array(experiment_data)
    experiment_std = numpy.array(experiment_std)

    # Base model parameters
    base_model_parameters = fit_parameters['fixed']

    # Loop over variable parameteres
    par_names = parameter_meshes.keys()
    results = []
    min_residual = 1.0e100
    for par_values in itertools.product(*[parameter_meshes[n] for n in par_names]):
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
        cleavage_data = [d[0]['phosphate_cleavage'] for d in data]
#        cleavage_data = [0.0112 * numpy.array(cd) for cd in cleavage_data]
        sampled_data = analysis.sampling.downsample_each(experiment_times, cleavage_data)
        sampled_data = [0.0112 * numpy.array(sd) for sd in sampled_data]
        cleavage_avg, cleavage_std = analysis.statistics.avg_std(sampled_data)

        # Calculate residual
        # add simulation variance to experiment variance
        residual_std = numpy.sqrt(cleavage_std**2 + experiment_std**2)
#        residual_std = experiment_std
        residual = fitpy.algorithms.common.residuals.chi_squared(
                experiment_times, experiment_data, residual_std, cleavage_avg) / len(cleavage_avg)
        if min_residual > residual:
            min_residual = residual
            print 'new min resid:', residual, 'pars:', par_values
#            best_length_avg, best_length_std = analysis.statistics.avg_std(
#                                analysis.sampling.downsample_each(experiment_times,
#                                    [d[0]['length'] for d in data]))
            best_cleavage_avg = cleavage_avg
            best_cleavage_std = cleavage_std
            best_par_values = par_values

#            best_d_concentration_avg, best_d_concentration_std = analysis.statistics.avg_std(
#                                analysis.sampling.downsample_each(experiment_times,
#                                    [d[0]['d_concentration'] for d in data]))
#
#            best_p_strand_count_avg, best_p_strand_count_std = analysis.statistics.avg_std(
#                                analysis.sampling.downsample_each(experiment_times,
#                                    [d[0]['p_strand_count'] for d in data]))
#
#            best_d_strand_count_avg, best_d_strand_count_std = analysis.statistics.avg_std(
#                                analysis.sampling.downsample_each(experiment_times,
#                                    [d[0]['d_strand_count'] for d in data]))
        results.append([pv for pv in par_values] + [residual])

    # Write csv file
    with open('test_output_file.csv', 'w') as f:
        # Write par names in order as comment
        f.write('#')
        for name in par_names:
            f.write(' %s' % name)
        f.write(' residual\n')

        # Write data
        w = csv.writer(f, delimiter=' ', lineterminator='\n')
        last_p1_value = None
        for row in results:
            if row[0] != last_p1_value:
                f.write('\n')
            w.writerow(row)
            last_p1_value = row[0]

    with open('cl_data.csv', 'w') as f:
        f.write('#')
        for name in par_names:
            f.write(' %s' % name)
        f.write('\n#')
        for par in best_par_values:
            f.write(' %f' % par)
        f.write('\n')

        w = csv.writer(f, delimiter=' ', lineterminator='\n')
        w.writerows(itertools.izip(experiment_times, experiment_data, experiment_std,
            best_cleavage_avg, best_cleavage_std))
#            best_length_avg, best_length_std,
#            best_d_concentration_avg, best_d_concentration_std,
#            best_p_strand_count_avg, best_p_strand_count_std,
#            best_d_strand_count_avg, best_d_strand_count_std))

baker.run()
