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

import argparse as _argparse

import tables as _tables

from IPython.Shell import IPShellEmbed as _IPShellEmbed

def _parse_command_line():
    parser = _argparse.ArgumentParser()
    parser.add_argument('--simulation_file', default='output.h5',
                        help='Simulation output pickle file name.')
    return parser.parse_args()

def _analyze_main():
    _args = _parse_command_line()

    # Read in hdf file
    hdf_file = _tables.openFile(filename=_args.simulation_file, mode='a')

    from actin_dynamics import analyses
    from actin_dynamics import visualization

    # Drop into shell
    banner = '\nWelcome to the actin dynamics analysis console.'

    global_namespace = {'hdf_file': hdf_file}
    local_namespace = {'analyses': analyses, 'visualization': visualization,
                       'root': hdf_file.getNode('/')}

    _shell = _IPShellEmbed(banner=banner)
    _shell(global_ns=global_namespace, local_ns=local_namespace)

    hdf_file.close()

if '__main__' == __name__:
    _analyze_main()
