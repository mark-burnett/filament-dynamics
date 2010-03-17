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

import multiprocessing

def pool_sim(simulation, argument, num_runs=None, num_processes=None):
    """
    Uses multiprocessing to perform multiple simulations at once.
    'argument' is either a single strand used for num_runs simulations
        or it is a sequence of initial strands each used for one simulation.
    'num_runs' is the number of simulations to perform, only use this if
        'argument' is a single strand.
    'num_processes' determines the size of the multiprocessing pool
    """
    pool = None
    if num_processes:
        pool = multiprocessing.Pool(num_processes)
    else:
        pool = multiprocessing.Pool()

    try:
        results = None
        if num_runs:
            results = [pool.apply_async(simulation, (argument,))
                           for i in xrange(num_runs)]
            # Add a crazy long timeout (ms) to work around a python bug.
            # This lets us use CTRL-C to stop the program.
            results = [r.get(999999999999) for r in results]
        else:
            results = pool.map_async(simulation, argument)
            # Add a crazy long timeout (ms) to work around a python bug.
            # This lets us use CTRL-C to stop the program.
            results = results.get(999999999999)

        # Multiprocessing cleanup
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        # Handle CTRL-C
        pool.terminate()
        raise

    return results
