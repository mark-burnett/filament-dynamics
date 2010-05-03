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
import hydro_sim.transitions.events

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
        self.data = []
        pub.subscribe(self.increment,
                      hydro_sim.transitions.events.hydrolysis)

    def perform(self, time, strand):
        pass

    def increment(self, event):
        if (event.old_state in self.old_states and
            event.new_state in self.new_states):
            self.count += 1
            self.data.append((event.time, self.count))
