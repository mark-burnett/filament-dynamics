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
import copy
import cPickle
import itertools

import multiprocessing

from actin_dynamics import io, factories
from actin_dynamics.simulations import run_simulation

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

    parameters = io.parse_parameters_file(open(args.parameters))
    object_graph = io.parse_object_graph_file(open(args.object_graph))

    simulation_factory = factories.SimulationFactory(object_graph, parameters)

    pool = multiprocessing.Pool()

    try:
        async_results = []
        for s in simulation_factory:
            async_results.append(pool.apply_async(run_simulation, (s,)))

        # Add a crazy long timeout (ms) to work around a python bug.
        # This lets us use CTRL-C to stop the program.
        results = [r.get(999999999999) for r in async_results]

        pool.close()
        pool.join()
    except KeyboardInterrupt:
        # Handle CTRL-C
        pool.terminate()
        raise

    cPickle.dump(results, open(args.output_file, 'wb'), -1)

if '__main__' == __name__:
    cli_main()
