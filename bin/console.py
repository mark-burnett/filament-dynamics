#!/usr/bin/env ipython
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


import numpy
import pylab


from actin_dynamics import analysis
from actin_dynamics import visualization
from actin_dynamics import io

from actin_dynamics.io import database

def _parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.ini',
                        help='Configuration file name')
    return parser.parse_args()

_args = _parse_command_line()
io.db_config.setup_database(configobj.ConfigObj(_args.config))
