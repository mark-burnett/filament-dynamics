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

class Random(object):
    __slots__ = ['state']
    def __init__(self, state):
        self.state = state

    def full_count(self, strand):
        return len(strand.indices[self.state])

    def update_vicinity(self, index, strand, old_state):
        if strand[index] == self.state:
            return 1
        elif old_state == self.state:
            return -1
        return 0

class PointedNeighbor(object):
    def __init__(self, state, pointed_neighbor):
        self.state    = state
        self.neighbor = pointed_neighbor

    def full_count(self, strand):
        count = 0
        for i in strand.indices[self.state]:
            try:
                if self.neighbor == strand[i - 1]:
                    count += 1
            except IndexError:
                pass
        return count

    def update_vicinity(self, index, strand, old_state):
        count = 0
        try:
            if self.neighbor == strand[index - 1]:
                if strand[index] == self.state:
                    count += 1
                elif old_state == self.state:
                    count -= 1
        except IndexError:
            pass

        try:
            if self.state == strand[index + 1]:
                if self.neighbor == strand[index]:
                    count += 1
                elif self.neighbor == old_state:
                    count -= 1
        except IndexError:
            pass

        return count
