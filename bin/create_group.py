#!/usr/bin/env python

#    Copyright (C) 2010-2011 Mark Burnett
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

import elixir

from actin_dynamics import io, utils

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--group_name', default=None, help='Group_name.')
    parser.add_argument('--config', default='config.ini',
                        help='Configuration file name')
    return parser.parse_args()


def create_group(config_filename, group_name):
    io.db_config.setup_database(configobj.ConfigObj(config_filename))
    group = io.database.Group.get_or_create(name=group_name)
    group.revision = utils.get_mercurial_revision()
    elixir.session.commit()


if '__main__' == __name__:
    args = parse_command_line()
    create_group(args.config, args.group_name)
