#    Copyright (C) 2010-2011 Mark Burnett
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

import collections
import math
import random

from .numerical import utils

from .numerical import rate_bisect

SimulationState = collections.namedtuple('SimulationState',
                                         'filaments concentrations')

class Simulation(object):
    """
    Kinetic Monte Carlo simulation object.
    """
    __slots__ = ['transitions', 'observers', 'end_conditions',
                 'state', 'rng']
    def __init__(self, sample_period=None, transitions=None, observers=None,
                 concentrations=None, filaments=None, end_conditions=None,
                 rng=random.uniform):
        self.sample_period  = sample_period
        self.transitions    = transitions
        self.observers      = observers
        self.end_conditions = end_conditions
        self.rng            = rng

        self.state = Simulation(concentrations=concentrations,
                                filaments=filaments)


    def run(self):
        '''
        Perform the actual simulation, starting with initial_state.
        '''
        # NOTE Alias for a small speedup in cpython.
        ml = math.log

        results = {'filaments': {}, 'concentrations': {}}
        for observer in self.observers:
            observer.initialize(results)

        time = 0
        next_measurement_time = 0

        while not any(e(time, self.state) for e in self.end_conditions):
            running_R = list(utils.running_total(t.R(time, self.state)
                                                 for t in self.transitions))
            total_R = running_R[-1]

            dt = ml(1/self.rng(0, 1)) / total_R

            # This provides causal measurements
            if time + dt > next_measurement_time:
                for observer in self.observers:
                    observer.measure(next_measurement_time, self.state)
                next_measurement_time += self.sample_period
            time = time + dt

            # Choose transition
            transition_r = self.rng(0, total_R)
            transition_index, remaining_r = rate_bisect.rate_bisect(
                    transition_r, running_R)

            self.transitions[transition_index].perform(time, self.state,
                                                       remaining_r)

        return results
