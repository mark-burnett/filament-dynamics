#!/usr/bin/env python

#    Copyright (C) 2011 Mark Burnett
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

import argparse
import configobj

from actin_dynamics import io, factories, job_control, run_support

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--object_graph', default='object_graph.yaml',
                        help='Object graph definition file.')

    parser.add_argument('--config', default='config.ini',
                        help='Configuration file name')

    return parser.parse_args()


def setup_database(config_filename):
    io.db_config.setup_database(configobj.ConfigObj(config_filename))


def cli_main(object_graph_filename):
    object_graph = io.parse_object_graph_file(open(object_graph_filename))

    for job in job_control.job_iterator():
        simulation_factory = factories.simulation_generator(object_graph,
                                                            parameters)
        run_support.run_simulations(simulation_factory, job.group)
        job_control.complete_job(job)


if '__main__' == __name__:
    args = parse_command_line()

    setup_database(args.config)
    cli_main(args.object_graph)
