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
    # XXX Consider making these (ordered) sets instead of lists (performance).
    return collections.defaultdict(list)

class Filament(object):
    __slots__ = ['states', 'relative_state_indices', 'measurements',
                 'relative_shift', 'relative_boundary_indices']
    def __init__(self, iterable):
        self.states = collections.deque(iterable)
        self.measurements = collections.defaultdict(list)

        # this is added to indexes stored in indices to get absolute index.
        self.relative_shift = 0

        # generate relative indices
        # XXX Consider making these (ordered) sets instead of lists (performance).
        self.relative_state_indices = collections.defaultdict(list)
        self.relative_boundary_indices = collections.defaultdict(
                _ddict_factory)

        for i, state in enumerate(self.states):
            self.relative_state_indices[state].append(i)

        for barbed_state, indices in self.relative_state_indices.iteritems():
            for i in indices:
                if i > 0:
                    pointed_state = self.states[i - 1]
                    if barbed_state != pointed_state:
                        self.relative_boundary_indices[barbed_state][pointed_state].append(i)


    def grow_barbed_end(self, state):
        self.states.append(state)
        self._update_relative_indices(len(self.states) - 1, None, state)

    def shrink_barbed_end(self):
        old_state = self.states.pop()
        self._update_relative_indices(len(self.states), old_state, None)


    def grow_pointed_end(self, state):
        self.states.appendleft(state)
        self._update_relative_indices(0, None, state)
        self.relative_shift += 1

    def shrink_pointed_end(self):
        old_state = self.states.popleft()
        self._update_relative_indices(-1, old_state, None)
        self.relative_shift -= 1


    def containted_states(self):
        return self.relative_state_indices.keys()


    def state_count(self, state):
        return len(self.relative_state_indices[state])

    def boundary_count(self, barbed_state, pointed_state):
        return len(self.relative_boundary_indices[barbed_state][pointed_state])

    def non_boundary_state_count(self, barbed_state, pointed_state):
        return (len(self.relative_state_indices[barbed_state]) - 
                len(self.relative_boundary_indices[barbed_state][pointed_state]))


    def state_index(self, state, target_index):
        relative_index = self.relative_state_indices[state][target_index]
        return relative_index + self.relative_shift

    def boundary_index(self, barbed_state, pointed_state, target_index):
        relative_index = (self.relative_boundary_indices[barbed_state]
                                                        [pointed_state]
                                                        [target_index])
        return relative_index + self.relative_shift

    def non_boundary_state_index(self, barbed_state, pointed_state,
                                 target_index):
        relative_indices = [i for i in self.relative_state_indices[barbed_state]
                            if i not in (self.relative_boundary_indices
                                         [barbed_state][pointed_state])]
        if target_index >= len(relative_indices):
            print target_index, len(relative_indices), barbed_state, pointed_state
        relative_index = relative_indices[target_index]
        return relative_index + self.relative_shift


    def __setitem__(self, absolute_index, new_state):
        # Adjust for negative indices
        if absolute_index < 0:
            absolute_index = absolute_index + len(self)

        old_state = self.states[absolute_index]
        self.states[absolute_index] = new_state
        self._update_relative_indices(absolute_index, old_state, new_state)

    def __getitem__(self, absolute_index):
        return self.states[absolute_index]

    def __len__(self):
        return len(self.states)

    def __contains__(self, state):
        return state in self.containted_states()


    def _update_relative_indices(self, absolute_index, old_state, new_state):
        self._update_relative_state_indices(absolute_index, old_state, new_state)
        self._update_relative_boundary_indices(absolute_index, old_state, new_state)

    def _update_relative_state_indices(self, absolute_index, old_state, new_state):
        relative_index = absolute_index - self.relative_shift

        if old_state is not None:
            self.relative_state_indices[old_state].remove(relative_index)
        if new_state is not None:
            self.relative_state_indices[new_state].append(relative_index)

    def _update_relative_boundary_indices(self, absolute_index, old_state, new_state):
        relative_index = absolute_index - self.relative_shift

        if absolute_index > 0:
            pointed_neighbor = self[absolute_index - 1]
            if old_state is not None and old_state != pointed_neighbor:
                self.relative_boundary_indices[old_state][pointed_neighbor].remove(relative_index)
            if new_state is not None and new_state != pointed_neighbor:
                self.relative_boundary_indices[new_state][pointed_neighbor].append(relative_index)

        if absolute_index < len(self) - 1:
            barbed_neighbor  = self[absolute_index + 1]
            if old_state is not None and old_state != barbed_neighbor:
               self.relative_boundary_indices[barbed_neighbor][old_state].remove(relative_index + 1)
            if new_state is not None and new_state != barbed_neighbor:
               self.relative_boundary_indices[barbed_neighbor][new_state].append(relative_index + 1)
