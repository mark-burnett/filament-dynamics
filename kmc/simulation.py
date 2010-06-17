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

import random
import copy
import bisect

import math

import util

__all__ = ['Simulation']

class Simulation(object):
    """
    Kinetic Monte Carlo simulation object.
    """
    __slots__ = ['transitions', 'ecs', 'measurements']
    def __init__(self, transitions, measurements, end_conditions):
        """
        'transitions' list of transition objects.  Each object represents
            a set of possible state changes.
        'end_conditions' is either a single end condition or an iterable of end
            conditions (see 'end_conditions' module).
        """
        self.transitions  = transitions
        self.measurements = measurements
        self.ecs          = end_conditions
        # Make sure end conditions are iterable.
        try:
            iter(self.ecs)
        except:
            self.ecs = [self.ecs]

    def __call__(self, initial_state):
        return self.run(initial_state)

    def run(self, state):
        """
        Perform the actual simulation, starting with initial_state.
        """
        # XXX Aliases for a small speedup.
        ru  = random.uniform
        ml  = math.log
        bbl = bisect.bisect_left

        # Initialize.
        [e.reset() for e in self.ecs]
        time = 0

        while not any(e(time, state) for e in self.ecs):
            # Calculate partial sums of transition probabilities
            transition_R = [t.R(state) for t in self.transitions]
            running_R    = list(util.generators.running_total(transition_R))
            total_R      = running_R[-1]

            # Update simulation time
            time += ml(1/ru(0, 1)) / total_R

            # Figure out which transition to perform
            r = ru(0, total_R)
            j = bbl(running_R, r)

            # Perform transition
            self.transitions[j].perform(time, state, running_R[j] - r)

            # Perform measurements
            [m.perform(time, state) for m in self.measurements]

        return state, dict((m.label, m) for m in self.measurements)
