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

from util.generators import running_total

__all__ = ['Simulation']

class Simulation(object):
    """
    Kinetic Monte Carlo simulation object.
    """
    __slots__ = ['transitions', 'ecs']
    def __init__(self, transitions, end_conditions):
        """
        'transitions' list of transition objects.  Each object represents
            a set of possible state changes.
        'end_conditions' is either a single end condition or an iterable of end
            conditions (see 'end_conditions' module).
        """
        self.transitions = transitions
        self.ecs = end_conditions
        # Make sure end conditions are iterable.
        try:
            iter(self.ecs)
        except:
            self.ecs = [self.ecs]

    def run(self, initial_data):
        """
        Perform the actual simulation, starting with initial_data.
        """
        data = copy.copy(initial_data)

        # Initialize odds and ends
        time = 0
        [t.initialize(data) for t in self.transitions]
        [e.reset() for e in self.ecs]

        while not any(e(time, data) for e in self.ecs):
            # Calculate partial sums of transition probabilities
            transition_R = [t.R for t in self.transitions]
            running_R    = list(running_total(transition_R))
            total_R      = running_R[-1]

            # Update simulation time
            time += math.log(1/random.uniform(0, 1)) / total_R

            # Figure out which transition to perform
            r = random.uniform(0, total_R)
            j = bisect.bisect_left(running_R, r)

            # Perform transition
            self.transitions[j].perform(running_R[j] - r, time)

        return data
