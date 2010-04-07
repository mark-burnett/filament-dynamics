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

import random
import copy
import bisect

import math

__all__ = ['Simulation', 'SimulationSequence']

def _running_total(values):
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
    def __init__(self, transitions, end_conditions, data_collectors):
        """
        'transitions' list of transition objects.  Each object represents
            a set of possible state changes.
        'end_conditions' is either a single end condition or an iterable of end
            conditions (see 'end_conditions' module).
        'data_collectors' is a dictionary with string keys, and callable values
            that accept **kwargs.  These callables are passed locals()
            at each step.  All return values that are not None are saved
            and returned when the simulation is performed by 'run' (below).
        """
        self.transitions = copy.deepcopy(transitions)
        self.ecs = copy.deepcopy(end_conditions)
        self.dcs = data_collectors
        try:
            iter(self.ecs)
        except:
            self.ecs = [self.ecs]

    def __call__(self, initial_strand):
        return self.run(initial_strand)

    def run(self, initial_strand):
        """
        Perform the actual simulation, starting with initial_strand.
        """
        strand = copy.deepcopy(initial_strand)
        data = dict( (key, []) for key in self.dcs.keys() )
        # Alias
        transitions = self.transitions

        # Initialize odds and ends
        [t.initialize(strand) for t in transitions]
        sim_time = 0
        [e.reset() for e in self.ecs]

        try:
            while not any(e(strand=strand,sim_time=sim_time) for e in self.ecs):
                # Collect and store data
                for key, f in self.dcs.items():
                    result = f(locals())
                    if result is not None:
                        data[key].append(result)

                # calculate partial sums of transition probabilities
                transition_R = [t.R for t in transitions]
                running_R = list(_running_total(transition_R))
                total_R = running_R[-1]

                # calculate transition time
                tau = math.log(1/random.uniform(0, 1)) / total_R
                # figure out which transition to perform
                r = random.uniform(0, total_R)
                j = bisect.bisect_left(running_R, r)

                # perform transition
                transition_output = transitions[j].perform(running_R[j] - r)

                # update transition probabilities
                [a.update(transition_output) for a in transitions]
                # update simulation time
                sim_time += tau
        except IndexError:
            pass

        data['final_strand'] = strand
        return data

class SimulationSequence(object):
    """
        This chains multiple simulations together, using the 'final_strand'
    of each previous simulation as the initial_strand for the next.
    """
    def __init__(self, simulations):
        self.simulations = simulations

    def run(self, initial_strand):
        current_strand = initial_strand
        results = []
        for s in self.simulations:
            results.append(s.run(current_strand))
            current_strand = results[-1]['final_strand']

        return results

    def __call__(self, initial_strand):
        """
        Sets the random seed, then calls self.run(initial_strand).
        """
        return self.run(initial_strand)
