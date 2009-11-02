from rate_conversions import scale_rates, scale_multiple_rates
from states import ChemicalState
from strand import Strand

def simulate( tailsize, tailstate, hydro_rates, depoly_rates,
              poly_rate, poly_state, duration, dt ):
    pr = poly_rate * dt
    dr = scale_rates( depoly_rates, dt )
    hr = scale_multiple_rates( hydro_rates, dt )

    timesteps = int ( duration / dt )

    added   = 0
    removed = 0
    strand  = Strand( tailsize, tailstate )

    for i in xrange( timesteps ):
        # Add a new monomer
        if random.random() < pr:
            strand.append( ChemicalState.ATP )
            added += 1

        # Hydrolize the strand
        strand.evolve( hr )

        # Depolymerize
        state = strand.peek()
        if random.random() < depoly_rates[state]:
            strand.pop()
            removed += 1
