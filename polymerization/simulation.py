"""
    This module contains a stochastic simulation object for actin strands.
"""

import copy

__all__ = ['Simulation']

class Simulation(object):
    """
    Stochastic simulation object.
    """
    def __init__(self, poly, depoly, hydro, record, end):
        """
        'poly', and 'depoly' are functions that modify the strand and return
            the number of subunits added or removed from the strand
        'hydro' is a callable that performs hydrolysis on the strand and
            returns information about that process.
        'record' is a dictionary with arbitrary keys, and callable values
            that accept **kwargs.  These callables are passed locals()
            at each step.  All return values that are not None are saved
            and returned when the simulation is performed by 'run' (below).
        """
        self.poly   = poly
        self.depoly = depoly
        self.hydro  = hydro
        self.record = record
        self.end    = end

    def run(self, initial_strand):
        """
        Perform the actual simulation, starting with initial_strand.
        """
        # Initialize strand
        # Copy initial strand to avoid threading problems.
        strand = copy.copy(initial_strand)

        # Initialize data storage dictionary
        data = dict( (key, []) for key in self.record.keys() )

        poly_count   = 0
        depoly_count = 0
        hydro_stats  = None

        # Copy end conditions to prevent threading problems.
        end = copy.deepcopy(self.end)
        [e.reset() for e in end]
        while not any(e(**locals()) for e in end):
#        while not any(e(None) for e in end):
            print strand
            poly_count += self.poly(strand)
            try:
                depoly_count += self.depoly(strand)
            except IndexError:
                break
            hydro_stats = self.hydro(strand, hydro_stats)

            # Collect and store data
            for key, f in self.record.items():
                result = f(**locals())
                if result is not None:
                    data[key].append(result)

        return data
