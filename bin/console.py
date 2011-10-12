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

import numpy
import pylab

from IPython.Shell import IPShellEmbed

from actin_dynamics import database, visualization, job_control

from actin_dynamics.configuration import command_line_parsers
from actin_dynamics.configuration import ini_parsers


banner = '''
    Actin Dynamics Copyright (C) 2011  Mark Burnett
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; for details read the LICENSE file.'''

def console_main():
    # Make plotting interactive
    pylab.ion()

    # Prepare and drop into iPython shell.
    namespace = {'database': database,
                 'db_session': database.DBSession(),
                 'numpy': numpy,
                 'pylab': pylab,
                 'job_control': job_control,
                 'visualization': visualization}

    shell = IPShellEmbed(argv=[], banner=banner)
    shell(local_ns=namespace)

if '__main__' == __name__:
    namespace = command_line_parsers.worker_process()
    ini_parsers.setup_database(namespace.config)

    console_main()
