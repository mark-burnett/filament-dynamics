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

from hydro_sim import events

def State(object):
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

    def __init__(self, allowed_states, initial_strand, concentrations):
        # XXX will not work for pointed end stuff
        self.concentrations = concentrations
        self.strand         = initial_strand
        self.indices        = {}
        for s in allowed_states:
            self.indices[s] = [i for i, v in enumerate(self.strand) if v == s]

    def initialize(self, pub):
        self.pub = pub
        for k in self.concentrations.keys():
            self.concentrations[k].initialize(pub)

    def change_state(self, index, new_state):
        if old_state != new_state:
            old_state = self.strand[index]
            # XXX remove might be slow (should be faster than making a new list)
            # XXX i could probably speed this up by maintaining sorted lists
            self.indices[old_state].remove(index)
            self.indices[new_state].append(index)
            self.strand[index] = new_state
            self.pub.publish(events.state_change(index, old_state, new_state))

    def polymerize(self, new_state):
        self.strand.append(new_state)
        index = len(self.strand) - 1
        self.indices[new_state].append(index)
        self.pub.publish(events.polymerization(index, new_state))

    def depolymerize(self):
        state = self.strand.pop()
        index = len(self.strand)
        self.indices[state].remove(index)
        self.pub.publish(events.depolymerization(index, state))

    def __len__(self):
        return len(self.strand)

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
