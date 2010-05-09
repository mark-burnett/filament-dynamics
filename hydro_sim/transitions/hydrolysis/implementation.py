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
    def __init__(self, predicate, rate, new_state):
        self.predicate = predicate
        self.rate      = rate
        self.new_state = new_state
        self.count     = 0

        self._index_to_update = None
        self._old_state       = None

    def initialize(self, pub, strand):
        self.count = self.predicate.full_count(strand)
        # Subscribe to poly, depoly, and hydro events.
        pub.subscribe(self._update_polymerization, events.polymerization)
        pub.subscribe(self._update_depolymerization,
                      events.depolymerization)
        pub.subscribe(self._update_hydrolysis, events.state_change)

    def R(self, strand):
        if self._index_to_update is not None:
            self.count += self.predicate.update_vicinity(self._index_to_update,
                                                         strand,
                                                         self._old_state)
            self._index_to_update = None
            self._old_state       = None
        return self.count * self.rate

    def perform(self, time, strand, r):
        index = int(r / self.rate)
        strand.change_state(index, self.new_state, time)

    # XXX it seems important to check nearby indices for effect.
    def _update_hydrolysis(self, event):
        self._index_to_update = event.index
        self._old_state = event.old_state
    
    def _update_polymerization(self, event):
        if 'barbed' == event.end:
            self._index_to_update = len(self.strand) - 1
        else:
            raise NotImplementedError()

    def _update_depolymerization(self, event):
        if 'barbed' == event.end:
            self._index_to_update = len(self.strand) - 1
        else:
            raise NotImplementedError()
