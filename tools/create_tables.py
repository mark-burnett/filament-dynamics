#/usr/bin/env python

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

import argparse
import configobj

import elixir

from actin_dynamics import database_model as dbm

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.ini',
                        help='Configuration file name')
    return parser.parse_args()

def main():
    args = parse_command_line()

    config_parser = configobj.ConfigObj(args.config)
    db_co = dbm.ConfigObject.from_configobj(config_parser)

    elixir.metadata.bind = db_co.bind

    elixir.setup_all(True)

if '__main__' == __name__:
    main()
