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

from hydro_sim.transitions import events

#from util.ordered_set import OrderedSet

__all__ = ['Hydrolysis']

class Hydrolysis(object):
    __slots__ = ['pub', 'predicate', 'rate', 'new_state', 'offset',
                 'strand', 'indices', 'R']
    def __init__(self, predicate, rate, new_state):
        self.predicate = predicate
        self.rate      = rate
        self.new_state = new_state
        self.offset    = 0

    def initialize(self, pub, strand):
        self.pub     = pub
        self.strand  = strand
        self.indices = set(i for i in xrange(len(self.strand))
                             if self.predicate(self.strand, i))
        self.R = self.rate * len(self.indices)

        # Subscribe to poly, depoly, and hydro events.
        self.pub.subscribe(self._update_polymerization, events.polymerization)
        self.pub.subscribe(self._update_depolymerization,
                           events.depolymerization)
        self.pub.subscribe(self._update_hydrolysis, events.hydrolysis)

    def perform(self, time, r):
        # XXX Speed limiting
        # Figure out what part of the strand to update
        set_index = int(r/self.rate)
        # XXX it's probably this statement that is speed limiting.
        set_value = list(self.indices)[set_index]
        full_index = set_value + self.offset

        # Update the strand
        old_state = self.strand[full_index]
        self.strand[full_index] = self.new_state

        # Let everyone else know what changed
        self.pub.publish(events.hydrolysis(old_state, self.new_state, full_index, time))

    def _update_indices(self, position):
        # XXX This statement is speed limiting
        effected_indices = xrange(position - self.predicate.pointed_range,
                                  position + self.predicate.barbed_range + 1)
        for i in effected_indices:
            if self.predicate(self.strand, i):
                self.indices.add(i - self.offset)
            else:
                self.indices.discard(i - self.offset)
        self.R = self.rate * len(self.indices)

    def _update_hydrolysis(self, event):
        self._update_indices(event.position)
    
    def _update_polymerization(self, event):
        if 'barbed' == event.end:
            self._update_indices(len(self.strand)-1)
        else:
            raise NotImplementedError()
            self.offset += 1
            self._update_indices(0)

    def _update_depolymerization(self, event):
        if 'barbed' == event.end:
            pos = len(self.strand)
            self.indices.discard(pos)
            return self._update_indices(pos - 1)
        else:
            raise NotImplementedError()
            # XXX These two lines may be out of order.
            self.indices.discard(-self.offset)
            self.offset -= 1
            self._update_indices(0)
