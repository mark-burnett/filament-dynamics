#    Copyright (C) 2009 Mark Burnett
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

from kmc.measurements import *

class StateCounts(object):
    __slots__ = ['label', 'data']
    def __init__(self, label):
        self.label = label
        self.data  = []

    def perform(self, time, strand):
        results = {}
        for k, indices in strand.state_indices.items():
            results[k] = len(indices)
        self.data.append((time, results))

class TransitionCount(object):
    __slots__ = ['label', 'data', 'old_state', 'new_state', 'count',
                 '_last_old_count', '_last_new_count']
    def __init__(self, label, old_state, new_state):
        self.label     = label
        self.data      = [(0, 0)]
        self.old_state = old_state
        self.new_state = new_state

        self.count = 0

        self._last_old_count = -1
        self._last_new_count = -1

    def perform(self, time, strand):
        old_count = len(strand.state_indices[self.old_state])
        new_count = len(strand.state_indices[self.new_state])

        if (self._last_old_count - 1 == old_count and
            self._last_new_count + 1 == new_count):
            self.count += 1
            self.data.append((time, self.count))
        self._last_old_count = old_count
        self._last_new_count = new_count

class Concentration(object):
    __slots__ = ['label', 'species', 'data', 'previous_value']
    def __init__(self, label, species):
        self.label          = label
        self.species        = species
        self.data           = []
        self.previous_value = -1

    def perform(self, time, strand):
        current_value = strand.concentrations[self.species].value()
        if self.previous_value != current_value:
            self.previous_value = current_value
            self.data.append((time, current_value))
