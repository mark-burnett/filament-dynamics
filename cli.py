#!/usr/bin/env pypy
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
import os.path

from actin_dynamics import io, factories
from actin_dynamics import mp_support

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--object_graph', default='object_graph.yaml',
                        help='Object graph definition file.')
    parser.add_argument('--parameters', default='parameters.yaml',
                        help='Parameters file.')

    parser.add_argument('--output_filename', default=None,
                        help='Output filename.  Overrides prefix + extension.')

    parser.add_argument('--output_prefix', default='output',
                        help='Beginning of output filename.')
    parser.add_argument('--output_extension', default='sim',
                        help='Output filename extension.')
    parser.add_argument('--output_directory', default='.',
                        help='Output directory.')

    parser.add_argument('--num_sims', type=int, default=1,
                        help='Number of simulations per parameter set.')

    parser.add_argument('--process_number', type=int, default=1,
                        help='Which process in the set are we?.')
    parser.add_argument('--num_processes', type=int, default=1,
                        help='How many processes are running?.')

    parser.add_argument('--split_parameter', default=None,
                        help='Parameter name to divide processing across.')

    return parser.parse_args()


def cli_main(parameters_filename, object_graph_filename, process_number,
             num_processes, output_filename, num_sims, split_parameter):
    parameters = io.parse_parameters_file(open(parameters_filename),
                                          split_parameter,
                                          process_number, num_processes)
    object_graph = io.parse_object_graph_file(open(object_graph_filename))

    simulation_factory = factories.simulation_generator(object_graph,
                                                        parameters, num_sims)

    mp_support.run_simulations(simulation_factory, output_filename)


if '__main__' == __name__:
    args = parse_command_line()

    if args.output_filename:
        output_filename = os.path.join(args.output_directory,
                                       args.output_filename)
    else:
        output_filename = os.path.join(args.output_directory,
                                       args.output_prefix +
                                       str(args.process_number) +
                                       '.' + args.output_extension)

    cli_main(args.parameters, args.object_graph, args.process_number,
             args.num_processes, output_filename, args.num_sims,
             args.split_parameter)
