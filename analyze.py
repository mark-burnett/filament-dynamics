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

import cPickle
import csv
import baker

import util
import analysis

@baker.command(default=True)
def dump_csv(filename, stage_name, analysis_name,
             output_filename='',
             output_dir='',
             **kwargs):
    """
    Dump analysis results to csv file.
    :param filename: Pickle file containing simulation results.
    :param analysis_name: Which analysis to perform.
    :param stage_name: Which stage to analyze.
    :param output_filename: Where to write results, ''=default
    :param output_dir: Where to write results, ''=default
    """
    # Figure out what analysis to perform
    a = util.introspection.lookup_name(analysis_name, analysis)

    # Read in file
    with open(filename) as f:
        sim_results = cPickle.load(f)

    # Determine which stage to analyze
    simulation_config = sim_results['simulation_config']
    stage_index = util.config.choose_stage(simulation_config['stages'],
                                           stage_name)

    # Extract stage data.
    stage_data     = [d[stage_index] for d in sim_results['data']]
    stage_duration = util.config.get_duration(
            simulation_config['stages'][stage_index]['end_conditions'])

    # Perform analysis
    output = a.make_csv(stage_data, duration=stage_duration,
#                        data_file=open(util.io.data_filename(analysis_name)),
                        **kwargs)

    # Dump to csv file
    with open(util.io.make_filename(filename, output_dir,
                            output_filename, analysis_name) + '.csv', 'w') as f:
        w = csv.writer(f, delimiter=' ')
        w.writerows(output)

baker.run()