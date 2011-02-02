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

def parse_command_line():
    parser = argparse.ArgumentParser()

    parser.add_argument('--parameters', default='parameters.yaml',
                        help='Parameters file.')

    parser.add_argument('--group_name', default=None, help='Group_name.')

    parser.add_argument('--config', default='config.ini',
                        help='Configuration file name')

    return parser.parse_args()


def setup_database(config_filename):
    io.db_config.setup_database(configobj.ConfigObj(config_filename))


def create_jobs(parameters_filename, group_name):
    parameters = io.parse_parameters_file(open(parameters_filename))
    job_control.create_jobs(parameters, group_name)


if '__main__' == __name__:
    args = parse_command_line()

    setup_database(args.config)
    create_jobs(args.parameters, args.group_name)
