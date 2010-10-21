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

import argparse
import cPickle

from actin_dynamics import io, factories

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--object_graph', default='object_graph.yaml',
                        help='Object graph definition file.')
    parser.add_argument('--parameters', default='parameters.yaml',
                        help='Parameters file.')
    parser.add_argument('--output_file', default='output.pickle',
                        help='Output pickle file name.')
    return parser.parse_args()

def cli_main():
    args = parse_command_line()

    parameter_ranges = io.parse_parameters_file(open(args.parameters))
    parameters = factories.make_parameter_mesh_iterator(parameter_ranges)

    object_graph = io.parse_object_graph_file(open(args.object_graph))
    simulation_factory = factories.SimulationFactory(object_graph, parameters)

    results = [s.run() for s in simulation_factory]

    cPickle.dump(results, open(args.output, 'wb'), -1)

if '__main__' == __name__:
    cli_main()
