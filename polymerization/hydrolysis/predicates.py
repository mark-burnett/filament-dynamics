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
    def __init__(self, state):
        self.state = state
        self.barbed_range  = 0
        self.pointed_range = 0

    def __call__(self, strand, index):
        if len(strand) <= index:
            return False
        return self.state == strand[index]

class Cooperative(object):
    def __init__(self, state, pointed_neighbor):
        self.state    = state
        self.neighbor = pointed_neighbor
        self.barbed_range  = 1
        self.pointed_range = 0

    def __call__(self, strand, index):
        if len(strand) <= index:
            return False
        if 0 == index:
            return False
        return (self.state == strand[index] and
                self.neighbor == strand[index - 1])

class SingleIndex(object):
    def __init__(self, state, index):
        self.state = state
        self.index = index
        self.barbed_range  = 0
        self.pointed_range = 0

    def __call__(self, strand, index):
        if index > len(strand):
            return False
        return (self.index == index and
                self.state == strand[index])
