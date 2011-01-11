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

from IPython.Shell import IPShellEmbed as IPShellEmbed

def open_console():
    # Setup welcome message.
    banner = '\nWelcome to the actin dynamics analysis console.'

    # Create namespaces.
    from actin_dynamics import analysis
#    from actin_dynamics import visualization
    from actin_dynamics import io

    local_namespace  = {'analysis': analysis,
                        'io': io}
#                        'visualization': visualization}

    # Create shell.
    shell = IPShellEmbed(argv=[], banner=banner)
    shell(local_ns=local_namespace)

if '__main__' == __name__:
    open_console()
