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

"""
    This module contains a stochastic simulation object for actin strands.
"""

import copy
import random

__all__ = ['Simulation', 'SimulationSequence']

class Simulation(object):
    """
    Stochastic simulation object.
    """
    def __init__(self, poly, depoly, hydro, record, end): #, rng=random):
        """
        'poly', and 'depoly' are functions that modify the strand and return
            the number of subunits added or removed from the strand
        'hydro' is a callable that performs hydrolysis on the strand and
            returns information about that process.
        'record' is a dictionary with arbitrary keys, and callable values
            that accept **kwargs.  These callables are passed locals()
            at each step.  All return values that are not None are saved
            and returned when the simulation is performed by 'run' (below).
        'end' is either a single end condition or an iterable of end
            conditions (see 'end_conditions' module).
        """
        self.poly   = poly
        self.depoly = depoly
        self.hydro  = hydro
        self.record = record
        self.end    = copy.deepcopy(end)
        try:
            iter(self.end)
        except:
            self.end = [self.end]
#        self.rng = rng

    def __call__(self, initial_strand):
        """
        Sets the random seed, then calls self.run(initial_strand).
        """
#        self.rng.seed()
        return self.run(initial_strand)

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

        hydro_stats = None
        # Copy end conditions to prevent threading problems.
        [e.reset() for e in self.end]
        while not any(e(**locals()) for e in self.end):
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

        # Capture the final state of the simulation.
        data['final_strand'] = strand
        return data

class SimulationSequence(object):
    """
        This chains multiple simulations together, using the 'final_strand'
    of each previous simulation as the initial_strand for the next.
    """
    def __init__(self, simulations): #, rng=random):
        self.simulations = simulations
#        self.rng = rng

    def run(self, initial_strand):
        current_strand = copy.copy(initial_strand)
        results = []
        for s in self.simulations:
            results.append(s.run(current_strand))
            current_strand = copy.copy(results[-1]['final_strand'])

        return results

    def __call__(self, initial_strand):
        """
        Sets the random seed, then calls self.run(initial_strand).
        """
#        self.rng.seed()
        return self.run(initial_strand)
