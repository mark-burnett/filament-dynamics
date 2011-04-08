#    Copyright (C) 2011 Mark Burnett
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

import collections
import copy
import itertools

import numpy


def _iterate_pairs(lst):
    right = iter(lst)
    right.next() # skip one!
    left  = iter(lst)
    return itertools.izip(left, right)

def _iterate_etf(counts, states):
    for count, state in itertools.izip(counts, states):
        for value in itertools.repeat(state, count):
            yield value


class EdgeTrackingFilament(object):
    __slots__ = ['_states', '_counts', '_edges', '_state_counts', '_length',
                 '_barbed_segments', '_pointed_segments', 'measurements']
    def __init__(self, counts=None, states=None, max_state_length=15):
        if counts:
            self._counts = numpy.array(counts)
        else:
            self._counts = numpy.array([])

        if states:
            self._states = numpy.array(states, dtype='|S%i' % max_state_length)
        else:
            self._states = numpy.array([], dtype='|S%i' % max_state_length)

        self.measurements = collections.defaultdict(list)
        # XXX DI failures abound :(
        self._edges = numpy.cumsum(self._counts)

        self._length = sum(self._counts)

        self._state_counts = collections.defaultdict(int)
        for s in numpy.unique(self._states):
            self._state_counts[s] = self._counts[
                    numpy.nonzero(s == self._states)].sum()

        self._update_segment_tracker()

    def _update_segment_tracker(self):
        self._barbed_segments = collections.defaultdict(set)
        self._pointed_segments = collections.defaultdict(set)
        for s in self._state_counts.iterkeys():
            matching_segments = numpy.nonzero(self._states == s)[0]
            self._pointed_segments[s] = set(matching_segments + 1)
            self._barbed_segments[s] = set(matching_segments)
    
    def _discard_segment(self, state, segment_index):
        self._pointed_segments[state].discard(segment_index + 1)
        self._barbed_segments[state].discard(segment_index)

    def _track_segment(self, state, segment_index):
        self._pointed_segments[state].add(segment_index + 1)
        self._barbed_segments[state].add(segment_index)


    @classmethod
    def from_iterable(cls, iterable):
        counts = []
        states = []
        previous_state = None
        for i in iterable:
            if i is previous_state:
                counts[-1] += 1
            else:
                counts.append(1)
                states.append(i)
                previous_state = i
        return cls(counts=counts, states=states)

    # Basic built in functionality:
    def __getitem__(self, index):
        return self._states[self._get_containing_segment(index)]

    def __setitem__(self, index, new_state):
        index = self._make_index_positive(index)
        # Figure out where the action is
        segment_index = self._get_containing_segment(index)
        remaining_index = index - self._counts[:segment_index].sum()

        old_state = self._states[segment_index]
        self._state_counts[old_state] -= 1
        self._state_counts[new_state] += 1

        # Do a dance based on remaining_index and segment size
        # four possibilities: left edge, right edge, middle, single
        segment_size = self._counts[segment_index]
        switch = None
        # Case single
        if 1 == segment_size:
            switch = 'single'
            self._states[segment_index] = new_state
            self._discard_segment(old_state, segment_index)
            self._track_segment(new_state, segment_index)
            self._merge_neighbors(segment_index)
        else:
            # Case left edge
            if 0 == remaining_index:
                switch = 'left'
                self._set_left(segment_index, new_state)
            # Case right edge
            elif segment_size - 1 == remaining_index:
                switch = 'right'
                old_states = copy.copy(self._states)
                old_counts = copy.copy(self._counts)
                old_edges = copy.copy(self._edges)
                self._set_right(segment_index, new_state)
            elif remaining_index > segment_size:
                raise RuntimeError('This should never happen.')
            # Case middle
            else:
                switch = 'middle'
                self._set_middle(segment_index, new_state, remaining_index)
            self._update_segment_tracker()


    def _set_left(self, segment_index, new_state):
        self._counts[segment_index] -= 1
        new_edge = self._edges[segment_index] - self._counts[segment_index]
        self._counts = numpy.insert(self._counts, segment_index, 1)
        self._states = numpy.insert(self._states, segment_index,
                                    new_state)
        self._edges = numpy.insert(self._edges, segment_index,
                                   new_edge)
        self._merge_neighbors(segment_index)
    
    def _set_right(self, segment_index, new_state):
        self._counts[segment_index] -= 1
        self._counts = numpy.insert(self._counts, segment_index+1, 1)
        self._states = numpy.insert(self._states, segment_index+1,
                                    new_state)
        self._edges = numpy.insert(self._edges, segment_index+1,
                                   self._edges[segment_index])
        self._edges[segment_index] -= 1
        self._merge_neighbors(segment_index + 1)

    def _set_middle(self, segment_index, new_state, remaining_index):
        # In this case we use the existing segment as the left
        # segment, and add two new segments for center & right.
        original_size = self._counts[segment_index]
        original_edge = self._edges[segment_index]
        old_state = self._states[segment_index]

        left_size = remaining_index
        right_size = original_size - left_size - 1

        left_edge = original_edge - right_size - 1
        center_edge = left_edge + 1
        right_edge = original_edge

        self._counts[segment_index] = left_size
        self._edges[segment_index] = left_edge

        insert_indices = [segment_index+1, segment_index+1]
        self._counts = numpy.insert(self._counts, insert_indices,
                [1, right_size])
        self._edges = numpy.insert(self._edges, insert_indices,
                [center_edge, right_edge])
        self._states = numpy.insert(self._states, insert_indices,
                [new_state, old_state])


    def _recalc_sc(self, state):
        return self._counts[numpy.nonzero(self._states == state)].sum()


    def __len__(self):
        return self._length

    def __iter__(self):
        'Return an iterator over the current snapshot of the filament.'
        # Have to make copies to avoid inconsistencies
        ccounts = copy.copy(self._counts)
        cstates = copy.copy(self._states)
        return _iterate_etf(ccounts, cstates)


    # Transition interface
    def state_count(self, state):
        return self._state_counts[state]

    def boundary_count(self, barbed_state, pointed_state):
        bm = self._barbed_segments[barbed_state]
        pm = self._pointed_segments[pointed_state]
        return len(bm.intersection(pm))
#        bm = barbed_state == self._states
#        pm = pointed_state == self._states
#        return (bm[1:] * pm[:-1]).sum()


    def state_index(self, state, target_index):
        segment_indices = numpy.nonzero(self._states == state)[0]
        local_edges = numpy.cumsum(self._counts[segment_indices])
        local_index = numpy.searchsorted(local_edges, target_index, side='right')
        segment_index = segment_indices[local_index]

        reverse_position = local_edges[local_index] - target_index

        return self._edges[segment_index] - reverse_position

    def boundary_index(self, barbed_state, pointed_state, target_index):
        remaining = target_index + 1
        target = (pointed_state, barbed_state)
        for segment_index, current in enumerate(_iterate_pairs(self._states)):
            if current == target:
                remaining -= 1
                if 0 == remaining:
                    return self._edges[segment_index]

    # Polymerization interface
    def grow_barbed_end(self, state):
        self._state_counts[state] += 1
        self._length += 1

        if state == self._states[-1]:
            self._counts[-1] += 1
            self._edges[-1] += 1
        else:
            self._states = numpy.append(self._states, [state])
            self._counts = numpy.append(self._counts, [1])
            self._edges = numpy.append(self._edges, [self._edges[-1] + 1])
            self._update_segment_tracker()

    def grow_pointed_end(self, state):
        self._edges += 1
        self._state_counts[state] += 1
        self._length += 1

        if state == self._states[0]:
            self._counts[0] += 1
        else:
            self._states = numpy.append([state], self._states)
            self._counts = numpy.append([1], self._counts)
            self._edges = numpy.append([1], self._edges)
            self._update_segment_tracker()


    def shrink_barbed_end(self):
        state = self._states[-1]
        self._state_counts[state] -= 1
        self._length -= 1

        self._counts[-1] -= 1
        self._edges[-1] -= 1
        if 0 == self._counts[-1]:
            self._counts = self._counts[:-1]
            self._states = self._states[:-1]
            self._edges = self._edges[:-1]
            self._update_segment_tracker()

    def shrink_pointed_end(self):
        state = self._states[0]
        self._state_counts[state] -= 1
        self._length -= 1

        self._counts[0] -= 1
        self._edges[0] -= 1
        if 0 == self._counts[0]:
            self._counts = self._counts[1:]
            self._states = self._states[1:]
            self._edges = self._edges[1:] - 1
            self._update_segment_tracker()
        else:
            self._edges -= 1


    # Support functions
    def _make_index_positive(self, index):
        while index < 0:
            index += self._length
        return index

    def _get_containing_segment(self, index):
        if 0 == index or -1 == index:
            return index
        index = self._make_index_positive(index)
        return numpy.searchsorted(self._edges, index, side='right')

    def _merge_neighbors(self, segment_index):
        lower_bound = max(0, segment_index -1)
        upper_bound = min(segment_index + 1, len(self._states) - 1)
        delete_indexes = []
        for i in xrange(lower_bound, upper_bound):
            if self._states[i] == self._states[i+1]:
                self._counts[i+1] += self._counts[i]
                delete_indexes.append(i)

        if delete_indexes:
            self._counts = numpy.delete(self._counts, delete_indexes)
            self._states = numpy.delete(self._states, delete_indexes)
            self._edges = numpy.delete(self._edges, delete_indexes)
