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

from rate_conversions import scale_rates, scale_multiple_rates
from states import ChemicalState
from strand import Strand

def simulate( tailsize, tailstate, hydro_rates, depoly_rates,
              poly_rate, poly_state, duration, dt, data_collectors ):
    pr = poly_rate * dt
    dr = scale_rates( depoly_rates, dt )
    hr = scale_multiple_rates( hydro_rates, dt )

    timesteps = int( duration / dt )

    added   = 0
    removed = 0
    strand  = Strand( tailsize, tailstate )

    data = dict( (key, []) for key in data_collectors.keys() )

    for i in xrange( timesteps ):
        # Add a new monomer
        if mtrand.rand() < pr:
            strand.append( poly_state )
            added += 1

        # Hydrolize the strand
        strand.evolve( hr )

        # Depolymerize
        state = strand.peek()
        if mtrand.rand() < dr[state]:
            strand.pop()
            removed += 1

        # Collect and store data
        for key, f in data_collectors.items():
            result = f(strand, added, removed, i)
            if result is not None:
                data[key].append( result )

    return data
