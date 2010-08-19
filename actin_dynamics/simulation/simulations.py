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
    This module contains a general Kinetic Monte Carlo simulation.
"""

import copy
import bisect

import math

def running_total(values):
    """
    Generator that calculates a running total of a sequence.
    """
    total = 0
    for v in values:
        total += v
        yield total

class Simulation(object):
    """
    Kinetic Monte Carlo simulation object.
    """
    __slots__ = ['transitions', 'concentrations', 'explicit_measurements',
                 'end_conditions', 'strand_factory', 'rng']
    def __init__(self, transitions, concentrations, explicit_measurements,
                 end_conditions, strand_factory, rng):
        """
        'transitions' list of transition objects.  Each object represents
            a set of possible state changes.
        'end_conditions' is either a single end condition or an iterable of end
            conditions (see 'end_conditions' module).
        """
        self.transitions = transitions
        self.concentrations = concentrations
        self.explicit_measurements = explicit_measurements
        self.end_conditions = end_conditions
        self.strand_factory = strand_factory
        self.rng = rng

    def run(self):
        """
        Perform the actual simulation, starting with initial_state.
        """
        # XXX Aliases for a small speedup.
        ml  = math.log
        bbl = bisect.bisect_left

        # Initialize.
        strand = self.strand_factory.create()
        [e.reset() for e in self.end_conditions]
        time = 0

        while not any(e(time, strand, self.concentrations)
                      for e in self.end_conditions):
            # Calculate partial sums of transition probabilities
            transition_R = [t.R(strand, self.concentrations)
                            for t in self.transitions]
            running_R    = list(running_total(transition_R))
            total_R      = running_R[-1]

            # Update simulation time
            time += ml(1/self.rng(0, 1)) / total_R

            # Figure out which transition to perform
            r = self.rng(0, total_R)
            j = bbl(running_R, r)

            # Perform transition
            self.transitions[j].perform(time, strand, self.concentrations,
                                        running_R[j] - r)

            # Perform strand measurements
            for measurement in self.explicit_measurements:
                measurement.perform(time, strand)

        # Compile measurements
        results = {}
        for c in self.concentrations.itervalues():
            if c.measurement_label:
                results[c.measurement_label] = c.data
        for t in self.transitions:
            if t.measurement_label:
                results[t.measurement_label] = t.data
        for em in self.explicit_measurements:
            if em.measurement_label:
                results[em.measurement_label] = em.data

        return strand, results
