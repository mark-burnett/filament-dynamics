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
import collections

import random

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
    __slots__ = ['transitions', 'concentrations', 'measurements',
                 'end_conditions', 'filaments', 'rng', 'parameters']
    def __init__(self, transitions=None, concentrations=None, measurements=None,
                 end_conditions=None, filaments=None, parameters=None, rng=None):
        """
        'transitions' list of transition objects.  Each object represents
            a set of possible state changes.
        'end_conditions' is either a single end condition or an iterable of end
            conditions (see 'end_conditions' module).
        """
        self.transitions    = transitions
        self.concentrations = concentrations
        self.measurements   = measurements
        self.end_conditions = end_conditions
        self.filaments      = filaments
        self.parameters     = parameters
        self.rng            = rng

def run_simulation(sim):
    """
    Perform the actual simulation, starting with initial_state.
    """
    # XXX Aliases for a small speedup.
    ml  = math.log
    bbl = bisect.bisect_left
    if sim.rng is not None:
        rng = sim.rng
    else:
        rng = random.uniform

    # Initialize.
    [e.reset() for e in sim.end_conditions]
    time = 0

    while not any(e(time, sim.filaments, sim.concentrations)
                  for e in sim.end_conditions):
        # Calculate partial sums of transition probabilities
        # NOTE we are keeping the small_Rs here so they don't need to be
        #   recalculated to determine which filament undergoes transition.
        small_Rs = []
        transition_Rs = []
        for t in sim.transitions:
            local_Rs = t.R(sim.filaments, sim.concentrations)
            transition_Rs.append(sum(local_Rs))
            small_Rs.append(local_Rs)

        running_transition_R = list(running_total(transition_Rs))
        total_R   = running_transition_R[-1]

        # Update simulation time
        if total_R <= 0:
            print 'ENDING SIMULATION:  no possible events.'
            break;
        time += ml(1/rng(0, 1)) / total_R

        # Figure out which transition to perform
        transition_r = rng(0, total_R)
        transition_index = bbl(running_transition_R, transition_r)

        # Figure out which filament to perform it on
        filament_r = running_transition_R[transition_index] - transition_r
        running_filament_R = list(running_total(small_Rs[transition_index]))
        filament_index = bbl(running_filament_R, filament_r)

        # Perform transition
        state_r = running_filament_R[filament_index] - filament_r
        sim.transitions[transition_index].perform(time, sim.filaments,
                                    sim.concentrations, filament_index, state_r)

        # Perform filament measurements
        for measurement in sim.measurements:
            measurement.perform(time, sim.filaments)

    # Compile measurements
    concentration_measurements = {}
    for state, c in sim.concentrations.iteritems():
        concentration_measurements[state] = c.data

    raw_filaments = [f.states for f in sim.filaments]
    filament_measurements = [f.measurements for f in sim.filaments]

    return (sim.parameters, concentration_measurements,
            raw_filaments, filament_measurements)
