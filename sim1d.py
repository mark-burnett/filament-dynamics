#    Copyright (C) 2009 Mark Burnett
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

from numpy.random import mtrand

def simulate(strand, hydro_rates, depoly_rates, poly_rate, poly_state,
             steps, data_collectors):
    """
    Performs a 1d simulation that allows only one end to grow/shrink.

    'strand' is modified during the process
    'data_collectors' is a dict of callbacks with access to all local variables
                      see data_collectors.py, and runsim.py for examples

    returns the results of the data_collectors
    """

    # Tracks the current length of the strand (relative to the start).
    length  = 0

    # Initialize data storage dictionary
    data = dict( (key, []) for key in data_collectors.keys() )

    for iteration in xrange( steps ):
        # Add a new monomer
        if mtrand.rand() < poly_rate:
            strand.append(poly_state)
            length += 1

        # Hydrolize the strand
        strand.evolve(hydro_rates)

        # Depolymerize
        tipstate = strand.peek()
        if mtrand.rand() < depoly_rates[tipstate]:
            strand.pop()
            length -= 1

        # Collect and store data
        for key, f in data_collectors.items():
            result = f(**locals())
            if result is not None:
                data[key].append(result)

    return data
