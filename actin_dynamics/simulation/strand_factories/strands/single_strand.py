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

def _ddict_factory():
    # XXX Consider making these sets instead of lists for performance reasons.
    return collections.defaultdict(list)

class Strand(object):
    __slots__ = ['states', 'state_indices', 'boundary_indices']
    def __init__(self, iterable):
        self.states = list(iterable)

        # generate statistics/strand boundary info
        self.state_indices = collections.defaultdict(list)
        self.boundary_indices = collections.defaultdict(
                _ddict_factory)

        for i, state in enumerate(self.states):
            self.state_indices[state].append(i)

        for barbed_state, indices in self.state_indices.iteritems():
            for i in indices:
                if i > 0:
                    pointed_state = self.states[i - 1]
                    if barbed_state != pointed_state:
                        self.boundary_indices[barbed_state][pointed_state].append(i)

    def grow_barbed_end(self, state):
        self.states.append(state)
        self._update_statistics(len(self.states) - 1, None, state)

    def shrink_barbed_end(self):
        old_state = self.states.pop()
        self._update_statistics(len(self.states), old_state, None)


    def set_state(self, index, state):
        old_state = self.states[index]
        self.states[index] = state
        # Adjust for negative indices
        if index < 0:
            index = index + len(self)
        self._update_statistics(index, old_state, state)

    def get_state(self, index):
        return self.states[index]


    def __setitem__(self, index, item):
        self.set_state(index, item)

    def __getitem__(self, index):
        return self.get_state(index)

    def __len__(self):
        return len(self.states)


    def _update_statistics(self, index, old_state, new_state):
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
               self.boundary_indices[barbed_neighbor][old_state].remove(index+1)
            if new_state is not None and new_state != barbed_neighbor:
               self.boundary_indices[barbed_neighbor][new_state].append(index+1)
