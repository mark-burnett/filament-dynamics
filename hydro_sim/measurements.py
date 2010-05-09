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
from . import events

class TransitionEventCount(object):
    __slots__ = ['data', 'label', 'old_states', 'new_states', 'count']
    def __init__(self, label, old_states, new_states):
        """
        old_states and new_states are containers of states.
        """
        self.label      = label
        self.old_states = old_states
        self.new_states = new_states
        self.count      = 0

    def initialize(self, pub, strand):
        self.data = [(0, 0)]
        pub.subscribe(self.increment, events.state_change)

    def perform(self, time, strand):
        pass

    def increment(self, event):
        if (event.old_state in self.old_states and
            event.new_state in self.new_states):
            self.count += 1
            self.data.append((event.time, self.count))

class TipState(object):
    __slots__ = ['label', 'index', 'data']
    def __init__(self, label, end):
        self.label = label
        if 'barbed' == end.lower():
            self.index = -1
        elif 'pointed' == end.lower():
            self.index = 0
        else:
            raise RuntimeError('Illegal end specified.')

    def initialize(self, pub, strand):
        self.data = []
        self.perform(0, strand)

    def perform(self, time, strand):
        self.data.append((time, strand[self.index]))
