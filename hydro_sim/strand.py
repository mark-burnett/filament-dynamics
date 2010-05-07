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

import util
import itertools
import random

def MySuperStrand(object):
    # contains states of positions
    # contains positions of states
    # contains concentrations (or # available subunits)

    # first 2 allow for general transitions
    #   for random it is obvious
    #   example for cooperative transition.R, - (p, t) +
    #       1) look at transition from state 't' indices
    #       2) for each index, check whether pointed end neighbor is 'p'
    #       3) count += 1

    # third allows polymerization/depolymerization transitions

    class Concentrations(object):
        __slots__ = ['_free_monomers', '_ftc']
        def __init__(self, free_monomers, ftc):
            self._free_monomers = free_monomers
            self._ftc           = ftc

        def __getitem__(self, state):
            return self._ftc * self._free_monomers[state]

    def __init__(self, allowed_states, initial_strand, initial_concentrations,
                 filament_tip_concentration):
        # XXX will not work for pointed end stuff
        self._free_monomers = dict((s, int(initial_concentrations.get(s, 0)/
                                           filament_tip_concentration))
                                   for s in allowed_states)
        self.concentrations = Concentrations(self._free_monomers,
                                             filament_tip_concentration)

        self.strand         = initial_strand
        self.indices        = {}
        for s in allowed_states:
            self.indices[s] = [i for i, v in self.strand if v == s]

    def initialize(self, pub):
        self.pub = pub

    def change_state(self, index, new_state):
        if old_state != new_state:
            old_state = self.strand[index]
            # XXX remove might be slow (should be faster than making a new set)
            self.indices[old_state].remove(index)
            self.indices[new_state].append(index)
            self.strand[index] = new_state
            self.pub.publish(events.state_change(index, old_state, new_state))

    def append(self, new_state):
        if self.free_monomers[new_state] <= 0:
            raise RuntimeError('Not enough free monomers to polymerize %s.' % new_state)

        self._free_monomers[new_state] -= 1
        self.strand.append(new_state)
        index = len(self.strand)-1
        self.indices[new_state].append(index)
        self.pub.publish(events.polymerization(index, new_state))

    def pop(self):
        state = self.strand.pop()
        self._free_monomers[new_state] += 1
        index = len(self.strand)
        self.indices[state].remove(index)
        self.pub.publish(events.depolymerization(index, state))

def single_state(model_states, simulation_states, size):
    state = util.states.match(model_states, simulation_states)
    while True:
        # XXX watch out for the list/deque problem (pointed end effects)
        yield list(itertools.repeat(state, size))

def random_states(model_states, simulation_states, size):
    states = [util.states.match(model_states, s) for s in simulation_states]
    while True:
        # XXX watch out for the list/deque problem (pointed end effects)
        yield [random.choice(states) for n in xrange(size)]
