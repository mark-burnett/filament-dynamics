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

from hydro_sim import events

__all__ = ['Hydrolysis']

class Hydrolysis(object):
    __slots__ = ['predicate', 'rate', 'new_state', 'count',
                 '_index_to_update', '_old_state']
    def __init__(self, old_state, rate, new_state):
        self.rate      = rate
        self.old_state = old_state
        self.new_state = new_state
        self.count     = 0

        self._index_to_update = None
        self._old_state       = None

    def initialize(self, pub, strand):
        self.count = self._full_count(strand)
        # Subscribe to poly, depoly, and hydro events.
        pub.subscribe(self._update_polymerization, events.polymerization)
        pub.subscribe(self._update_depolymerization,
                      events.depolymerization)
        pub.subscribe(self._update_hydrolysis, events.state_change)

    def R(self, strand):
        if self._index_to_update is not None:
            self.count += self._update_vicinity(strand)
            self._index_to_update = None
            self._old_state       = None
        return self.count * self.rate

    def perform(self, time, strand, r):
        state_index = int(r / self.rate)
        index = strand.indices[self.old_state][state_index]
        strand.change_state(index, self.new_state, time)

    # XXX it seems important to check nearby indices for effect.
    def _update_hydrolysis(self, event):
        self._index_to_update = event.index
        self._old_state = event.old_state
    
    def _update_polymerization(self, event):
        if event.index > 0:
            self._index_to_update = event.index - 1
        else:
            raise NotImplementedError()

    def _update_depolymerization(self, event):
        if event.index > 0:
            self._index_to_update = event.index - 1
        else:
            raise NotImplementedError()

class Random(Hydrolysis):
    def _full_count(self, strand):
        return len(strand.indices[self.old_state])

    def _update_vicinity(self, strand):
        if strand[self._index_to_update] == self.old_state:
            return 1
        elif self._old_state == self.old_state:
            return -1
        return 0
