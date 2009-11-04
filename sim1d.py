from numpy import random

from rate_conversions import scale_rates, scale_multiple_rates
from states import ChemicalState
from strand import Strand

def simulate( tailsize, tailstate, hydro_rates, depoly_rates,
              poly_rate, poly_state, duration, dt, data_collectors ):
    pr = poly_rate * dt
    dr = scale_rates( depoly_rates, dt )
    hr = scale_multiple_rates( hydro_rates, dt )

    timesteps = int ( duration / dt )

    added   = 0
    removed = 0
    strand  = Strand( tailsize, tailstate )

    data = dict( (key, []) for key in data_collectors.keys() )

    for i in xrange( timesteps ):
        # Add a new monomer
        if random.random() < pr:
            strand.append( ChemicalState.ATP )
            added += 1

        # Hydrolize the strand
        strand.evolve( hr )

        # Depolymerize
        state = strand.peek()
        if random.random() < dr[state]:
            strand.pop()
            removed += 1

        # Collect and store data
        for key, f in data_collectors.items():
            result = f(strand, added, removed, i)
            if result is not None:
                data[key].append( result )

    return data
