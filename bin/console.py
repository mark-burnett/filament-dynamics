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

import copy

import elixir

import numpy
import pylab

from IPython.Shell import IPShellEmbed

from actin_dynamics import analysis
from actin_dynamics import visualization
from actin_dynamics import io

from actin_dynamics.io import database


banner = '''
Welcome to the actin dynamics interactive console!'''

def get_database_dict():
    result = copy.copy(database.__dict__)
    for name in result.keys():
        if '_' == name[0]:
            del result[name]
    return result

def console_main():
    io.db_config.setup_database()

    namespace = get_database_dict()
    namespace['elixir'] = elixir
    namespace['visualization'] = visualization
    namespace['analysis'] = analysis
    namespace['numpy'] = numpy
    namespace['pylab'] = pylab

    shell = IPShellEmbed(argv=[], banner=banner)
    shell(local_ns=namespace)

if '__main__' == __name__:
    console_main()
