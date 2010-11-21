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

from actin_dynamics import io, factories
from actin_dynamics import mp_support

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--object_graph', default='object_graph.yaml',
                        help='Object graph definition file.')
    parser.add_argument('--parameters', default='parameters.yaml',
                        help='Parameters file.')
    parser.add_argument('--output_file', default='output.h5',
                        help='Output pickle file name.')
    parser.add_argument('--num_sims', default=1,
                        help='Number of simulations per parameter set.')
    return parser.parse_args()

def cli_main():
    args = parse_command_line()

    parameters = io.parse_parameters_file(open(args.parameters))
    object_graph = io.parse_object_graph_file(open(args.object_graph))

#    simulation_factory = factories.SimulationFactory(object_graph, parameters)
    simulation_factory = factories.simulation_generator(object_graph,
                                                        parameters,
                                                        args.num_sims)

    mp_support.run_simulations(simulation_factory, args.output_file)
    # NOTE used for profiling
#    mp_support.sp_run_simulations(simulation_factory, args.output_file)

if '__main__' == __name__:
    cli_main()
