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

from actin_dynamics import io
from actin_dynamics import job_control

def parse_command_line(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--parameters', default='parameters.yaml',
                        help='Parameters file.')

    parser.add_argument('--object_graph', default='object_graph.yaml',
                        help='Object Graph file.')

    parser.add_argument('--group_name', default=None, help='Group_name.')

    return parser.parse_args(args)


def setup_database(config_filename):
    io.db_config.setup_database(configobj.ConfigObj(config_filename))


def create_jobs(parameters_filename, object_graph_filename, group_name):
    parameters = io.parse_parameters_file(open(parameters_filename))
    object_graph_yaml = open(object_graph_filename).read()
    job_control.create_jobs(parameters, object_graph_yaml, group_name)


if '__main__' == __name__:
    remaining_argv = io.db_config.setup_database()
    args = parse_command_line(remaining_argv)

    create_jobs(args.parameters, args.object_graph, args.group_name)
