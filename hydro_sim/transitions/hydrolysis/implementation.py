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

from util.ordered_set import OrderedSet

__all__ = ['Hydrolysis']

class Hydrolysis(object):
    __slots__ = ['pub', 'predicate', 'rate', 'new_state', 'offset',
                 'strand', 'indices', 'R']
    def __init__(self, pub, predicate, rate, new_state):
        self.pub       = pub
        self.predicate = predicate
        self.rate      = rate
        self.new_state = new_state
        self.offset    = 0

        # Subscribe to poly, depoly, and hydro events.
        self.pub.add(self._update_polymerization,   events.polymerization)
        self.pub.add(self._update_depolymerization, events.depolymerization) 
        self.pub.add(self._update_hydrolysis,       events.hydrolysis)

    def initialize(self, strand):
        self.strand = strand
        self.indices = OrderedSet(i for i in xrange(len(self.strand))
                                  if self.predicate(self.strand, i))
        self.R = self.rate * len(self.indices)

    def perform(self, r, time):
        # Figure out what part of the strand to update
        set_index = int(r/self.rate)
        set_value = self.indices[set_index]
        full_index = set_value + self.offset

        # Update the strand
        # XXX breaks here
        try:
            old_state = self.strand[full_index]
        except:
            print set_index, set_value, full_index, len(self.indices)
            raise
        self.strand[full_index] = self.new_state

        # Remove this index
        # XXX i don't have to do this here, it will happen on update anyway..
#        self.indices.remove(set_value)

        # Let everyone else know what changed
        self.pub.publish(events.hydrolysis(old_state, self.new_state, full_index, time))

    def _update_indices(self, position):
        effected_indices = xrange(position - self.offset - self.predicate.pointed_range,
                                  position - self.offset + self.predicate.barbed_range + 1)
        for i in effected_indices:
            if self.predicate(self.strand, i):
                self.indices.add(i)
            else:
                self.indices.discard(i)
        self.R = self.rate * len(self.indices)

    def _update_hydrolysis(self, event):
        self._update_indices(event.position)
    
    def _update_polymerization(self, event):
        if 'barbed' == event.end:
            self._update_indices(len(self.strand)-1)
        else:
            self.offset += 1
            self._update_indices(0)

    def _update_depolymerization(self, event):
        if 'barbed' == event.end:
            pos = len(self.strand)
            self.indices.discard(pos)
            return self._update_indices(pos - 1)
        else:
            raise NotImplementedError()
            # XXX this code is wrong for sure.
            self.offset -= 1
            self.indices.discard(0)
            self._update_indices(0)
