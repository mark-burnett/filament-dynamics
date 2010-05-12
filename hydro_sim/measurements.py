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

class StateFractions(object):
    __slots__ = ['label', 'data']
    def __init__(self, label):
        self.label = label
        self.data  = []

    def perform(self, time, strand):
        results = {}
        for k, indices in strand.state_indices.items():
            results[k] = len(indices)
        self.data.append((time, results))

class ConcentrationMonitor(object):
    __slots__ = ['label', 'data', 'state', 'last_concentration']
    def __init__(self, label, state):
        self.label = label
        self.state = state
        self.data  = []
        self.last_concentration = -1

    def perform(self, time, strand):
        v = strand.concentrations[self.state].value()
        if self.last_concentration != v:
            self.data.append((time, v))

class TransitionEventCount(object):
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
            self.data.append((time, self.count))
        else:
            self._last_old_count = old_count
            self._last_new_count = new_count

class TipState(object):
    __slots__ = ['label', 'index', 'data', 'last_state']
    def __init__(self, label, index):
        self.label      = label
        self.index      = index
        self.last_state = None
        self.data       = []

    def perform(self, time, strand):
        if self.last_state != strand[self.index]:
            self.data.append((time, strand[self.index]))
