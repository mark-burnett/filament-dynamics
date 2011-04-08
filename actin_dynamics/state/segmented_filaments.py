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

import itertools
import collections

def iterate_pairs(lst):
    right = iter(lst)
    right.next() # skip one!
    left  = iter(lst)
    return itertools.izip(left, right)


class BasicSegment(object):
    __slots__ = ['state', 'count']
    def __init__(self, state, count):
        self.state = state
        self.count = count

    def __iter__(self):
        return itertools.repeat(self.state, self.count)

    def __len__(self):
        return self.count

    def __repr__(self):
        return '%s(state=%s, count=%s)' % (self.__class__.__name__,
                self.state, self.count)


    def decrement(self):
        '''
        Decreases the count of this segment and returns replacement segments.
        '''
        self.count -= 1
        if self.count:
            return [self]
        return []

    def fracture(self, index, new_state):
        '''
            Replaces state with new_state at index, and returns upto 3
        new segments to replace this segment.
        '''
        result_segments = []
        if index > 0:
            result_segments.append(BasicSegment(state=self.state, count=index))
        result_segments.append(BasicSegment(state=new_state, count=1))
        if self.count > index + 1:
            result_segments.append(BasicSegment(state=self.state,
                                                count=(self.count - index - 1)))
        return result_segments

    def merge(self, barbed_neighbor):
        '''
            Joins this segment with its barbed neighbor if their states match.
        Returns the list of segments that replace this segment + neighbor.
        '''
        if self.state == barbed_neighbor.state:
            return [BasicSegment(state=self.state,
                                count=(self.count + barbed_neighbor.count))]
        else:
            return [self, barbed_neighbor]

def _segmentize(iterable):
    i = iter(iterable)
    segments = [BasicSegment(state=i.next(), count=1)]
    for v in i:
        if v == segments[-1].state:
            segments[-1].count += 1
        else:
            segments.append(BasicSegment(state=v, count=1))

    return segments


class SegmentedFilament(object):
    __slots__ = ['segments', 'measurements', '_length']
    def __init__(self, *segments):
        self.segments = list(segments)
        self.measurements = collections.defaultdict(list)
        self._length = sum(map(len, self.segments))

    @classmethod
    def from_iterable(cls, iterable):
        return cls(*_segmentize(iterable))

    def __iter__(self):
        return itertools.chain(*self.segments)

    def __len__(self):
        return self._length

    def __getitem__(self, index):
        if (0 == index) or (-1 == index):
            return self.segments[index].state
        if index < 0:
            index = len(self) + index
        # XXX Watch for exception if index not found.
        try:
            segment_index, segment, remaining_index = (
                    self._get_containing_segment(index))
            return segment.state
        except IndexError:
            pass

    def __setitem__(self, index, value):
        if index < 0:
            index = len(self) + index
        # XXX Watch for exception if index not found.
        segment_index, segment, remaining_index = (
                self._get_containing_segment(index))

        new_segments = segment.fracture(remaining_index, value)
        self._merge_segments(segment_index, new_segments)

    def _merge_segments(self, segment_index, new_segments):
        left_index = segment_index
        right_index = segment_index + 1

        # Left merge
        if segment_index > 0:
            new_segments[0:1] = self.segments[segment_index-1].merge(
                    new_segments[0])
            left_index -= 1

        # Right merge
        if segment_index < len(self.segments) - 1:
            new_segments[-1:] = new_segments[-1].merge(
                    self.segments[segment_index+1])
            right_index += 1

        self.segments[left_index:right_index] = new_segments


    def _get_containing_segment(self, state_index, target_state=None,
                                penalize_neighbor=object()):
        remaining = state_index
        previous_segment = self.segments[0]
        for segment_index, segment in enumerate(self.segments):
            if (target_state is None or target_state == segment.state):
                if penalize_neighbor is previous_segment.state:
                    remaining += 1
                if remaining < segment.count:
                    return segment_index, segment, remaining
                remaining -= segment.count
            previous_segment = segment
        raise IndexError('State not found.')


    def state_count(self, state):
        count = 0
        for segment in self.segments:
            if state == segment.state:
                count += segment.count
        return count

    def state_index(self, state, target_index):
        if target_index < 0:
            target_index = len(self) + target_index
        segment_index, segment, remaining_index = (
                self._get_containing_segment(target_index, target_state=state))
        base_index = sum(map(len, self.segments[:segment_index]))
        return base_index + remaining_index


    def boundary_index(self, barbed_state, pointed_state, target_index):
        remaining = target_index + 1
        index = 0
        for pointed_segment, barbed_segment in iterate_pairs(self.segments):
            if (barbed_state  == barbed_segment.state and
                pointed_state == pointed_segment.state):
                remaining -= 1
            index += pointed_segment.count
            if not remaining:
                return index
        raise IndexError('Boundary not found.')

    def boundary_count(self, barbed_state, pointed_state):
        count = 0
        target = [pointed_state, barbed_state]
        for current in iterate_pairs(self.segments):
            if current == target:
                count += 1
        return count

#    def non_boundary_state_index(self, state, pointed_neighbor, target_index):
#        total = self.state_count(state) - self.boundary_count(state,
#                                                              pointed_neighbor)
#        if target_index < 0:
#            target_index = total + target_index
#
#        segment_index, segment, remaining_index = (
#                self._get_containing_segment(target_index, target_state=state,
#                                             penalize_neighbor=pointed_neighbor))
#
#        base_index = sum(map(len, self.segments[:segment_index]))
#        return base_index + remaining_index

    def grow_barbed_end(self, state):
        end_segments = self.segments[-1].merge(BasicSegment(state=state, count=1))
        self.segments[-1:] = end_segments
        self._length += 1

    def grow_pointed_end(self, state):
        end_segments = BasicSegment(state=state, count=1).merge(self.segments[0])
        self.segments[0:1] = end_segments
        self._length += 1


    def shrink_barbed_end(self):
        self.segments[-1:] = self.segments[-1].decrement()
        self._length -= 1

    def shrink_pointed_end(self):
        self.segments[0:1] = self.segments[0].decrement()
        self._length -= 1
