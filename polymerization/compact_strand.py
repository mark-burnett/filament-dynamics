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

from collections import deque

__all__ = ['CompactStrand', 'cleanup_substrands']

def strand_iterator(substrands):
    for s in substrands:
        for k in xrange(s[0]):
            yield s[1]

def reverse_strand_iterator(substrands):
    rsubstrands = reversed(substrands)
    for s in rsubstrands:
        for k in xrange(s[0]):
            yield s[1]

def cleanup_substrands(substrands):
    cleaned = []
    for s in substrands:
        if cleaned:
            last_s = cleaned[-1]
            if last_s[1] == s[1]:
                cleaned[-1] = (last_s[0] + s[0], s[1])
            else:
                cleaned.append(s)
        else:
            cleaned.append(s)
    return deque(cleaned)

class CompactStrand(object):
    """
    Single ended strand for studying filament tip dynamics.
    This object is meant to have an interface like a normal python deque,
    despite a compressed internal structure.
    """
    def __init__(self, tailsize, tailstate):
        self.substrands = deque([(tailsize, tailstate)])

    # Representation operators
    def __str__(self):
        return str(self.substrands)

    def __repr__(self):
        return str(self)

    # Accessors
    def __getitem__(self, i):
        """
        This can be significantly optimized, but I don't need that right now.
        """
        if i >= 0:
            si = strand_iterator(self.substrands)
            for j in xrange(i):
                si.next()
            return si.next()
        else:
            si = reverse_strand_iterator(self.substrands)
            m = -i - 1
            for j in xrange(m):
                si.next()
            return si.next()

    # Addition and removal operators
    def append(self, state):
        """
        Adds an element in the given state to the tail end of the strand.
        """
        end = self.substrands[-1]
        if end[1] == state:
            self.substrands[-1] = (end[0] + 1, state)
        else:
            self.substrands.append( (1, state) )

    def appendleft(self, state):
        """
        Adds an element in the given state to the tail end of the strand.
        """
        end = self.substrands[0]
        if end[1] == state:
            self.substrands[0] = (end[0] + 1, state)
        else:
            self.substrands.appendleft( (1, state) )

    def pop(self):
        """
        Returns and removes one element from the end of the strand.
        """
        end = self.substrands[-1]
        st = end[1]
        if 1 == end[0]:
            del self.substrands[-1]
        else:
            self.substrands[-1] = (end[0] - 1, st)
        if not self.substrands:
            print "holy shit batman, we emptied the reservior."
            raise self
        return st

    def popleft(self):
        """
        Returns and removes one element from the end of the strand.
        """
        end = self.substrands[0]
        st = end[1]
        if 1 == end[0]:
            del self.substrands[0]
        else:
            self.substrands[0] = (end[0] - 1, st)
        if not self.substrands:
            print "holy shit batman, we emptied the reservior."
            raise self
        return st

    # Misc list operators
    def reverse(self):
        self.substrands.reverse()

    def __len__(self):
        num = 0
        for sub in self.substrands:
            num += sub[0]
        return num

    def __iter__(self):
        return strand_iterator(self.substrands)
