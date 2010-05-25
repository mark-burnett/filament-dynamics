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

class Strand(list):
    __slots__ = ['state_indices', 'boundary_indices']
    def __init__(self, states, initial_strand):
        list.__init__(self, initial_strand)
#        self.extend(initial_strand)
        self.state_indices    = {}
        self.boundary_indices = collections.defaultdict(dict)

        for s in states:
            self.state_indices[s] = [i for i, v in enumerate(self) if v == s]

        for sb, sp in itertools.product(states, states):
            if sb != sp:
                self.boundary_indices[sb][sp] = [i for i in self.state_indices[sb]
                                                   if i > 0 and
                                                   self[i - 1] == sp]

    def append(self, item):
        list.append(self, item)
        self._update(len(self) - 1, None, item)

    def pop(self):
        old_state = list.pop(self)
        self._update(len(self), old_state, None)

    def __setitem__(self, index, value):
        old_state = self[index]
        list.__setitem__(self, index, value)
        while index < 0:
            index = index + len(self)
        self._update(index, old_state, value)

    def _update(self, index, old_state, new_state):
        self._update_state_indices(   index, old_state, new_state)
        self._update_boundary_indices(index, old_state, new_state)

    def _update_state_indices(self, index, old_state, new_state):
        if old_state is not None:
            self.state_indices[old_state].remove(index)
        if new_state is not None:
            self.state_indices[new_state].append(index)

    def _update_boundary_indices(self, index, old_state, new_state):
        if index > 0:
            pointed_neighbor = self[index - 1]
            if old_state is not None and old_state != pointed_neighbor:
                self.boundary_indices[old_state][pointed_neighbor].remove(index)
            if new_state is not None and new_state != pointed_neighbor:
                self.boundary_indices[new_state][pointed_neighbor].append(index)

        if index < len(self) - 1:
            barbed_neighbor  = self[index + 1]
            if old_state is not None and old_state != barbed_neighbor:
                self.boundary_indices[barbed_neighbor][old_state].remove(index + 1)
            if new_state is not None and new_state != barbed_neighbor:
                self.boundary_indices[barbed_neighbor][new_state].append(index + 1)

def single_state(model_states, state=None, length=None,
                 seed_concentration=None, filament_tip_concentration=None):
    if not state:
        raise RuntimeError("'state' not specified.")

    if length:
        size = int(length)
    elif seed_concentration and filament_tip_concentration:
        size = int(seed_concentration / filament_tip_concentration)
    else:
        raise RuntimeError('Indeterminite size.')

    while True:
        yield Strand(model_states, itertools.repeat(state, size))

def random_states(model_states, states=None, length=None,
                  seed_concentration=None, filament_tip_concentration=None):
    if not states:
        raise RuntimeError("'states' not specified.")

    if length:
        size = int(length)
    elif seed_concentration and filament_tip_concentration:
        size = int(seed_concentration / filament_tip_concentration)
    else:
        raise RuntimeError('Indeterminite size.')

    while True:
        yield Strand(model_states, (random.choice(states) for n in xrange(size)))
