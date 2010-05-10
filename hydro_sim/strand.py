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

import itertools
import collections

import util

class Strand(object):
    def __init__(self, states, initial_strand, concentrations):
        self._sequence        = initial_strand
        self.concentrations   = concentrations
        self.state_indices    = {}
        self.boundary_indices = collections.defaultdict(dict)

        for s in states:
            self.state_indices[s] = [i for i, v in enumerate(self._sequence)
                                       if v == s]

        for sb, sp in itertools.product(states, states):
            if sb != sp:
                self.boundary_indices[sb][sp] = [i for i in self.state_indices[sb]
                                                   if i > 0 and
                                                   self._sequence[i - 1] == sp]

    def append(self, item):
        self.concentrations[item].polymerize()
        self._sequence.append(item)
        self._update(len(self._sequence) - 1, None, item)

    def pop(self):
        old_state = self._sequence.pop()
        self.concentrations[old_state].polymerize()
        self._update(len(self._sequence), old_state, None)

    def __getitem__(self, index):
        return self._sequence[index]

    def __setitem__(self, index, value):
        old_state = self._sequence[index]
        self._sequence[index] = value
        while index < 0:
            index = index + len(self._sequence)
        self._update(index, old_state, value)

    def __len__(self):
        return len(self._sequence)

    def _update(self, index, old_state, new_state):
        self._update_state_indices(index, old_state, new_state)
        self._update_boundary_indices(index, old_state, new_state)

    def _update_state_indices(self, index, old_state, new_state):
        if old_state is not None:
            self.state_indices[old_state].remove(index)
        if new_state is not None:
            self.state_indices[new_state].append(index)

    def _update_boundary_indices(self, index, old_state, new_state):
        if index > 0:
            pointed_neighbor = self._sequence[index - 1]
            if old_state is not None and old_state != pointed_neighbor:
                self.boundary_indices[old_state][pointed_neighbor].remove(index)
            if new_state is not None and new_state != pointed_neighbor:
                self.boundary_indices[new_state][pointed_neighbor].append(index)

        if index < len(self._sequence) - 1:
            barbed_neighbor  = self._sequence[index + 1]
            if old_state is not None and old_state != barbed_neighbor:
                self.boundary_indices[barbed_neighbor][old_state].remove(index + 1)
            if new_state is not None and new_state != barbed_neighbor:
                self.boundary_indices[barbed_neighbor][new_state].append(index + 1)

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
