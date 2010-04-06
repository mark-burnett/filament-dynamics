#    Copyright (C) 2010 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by #    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

__all__ = ['Transition', 'BarbedPolymerization', 'BarbedDepolymerization']

class Transition(object):
    def __init__(self, predicate, rate, new_state):
        self.predicate = predicate
        self.rate = rate
        self.new_state = new_state

    def initialize(self, strand):
        self._update_switch = {'transition': self._update_transition,
                               'poly':       self._update_polymerization,
                               'depoly':     self._update_depolymerization}
        self.strand = strand
        # FIXME no offset precludes pointed end polymerization
#        self.offset = 0
        self.indices = set(i for i in xrange(len(self.strand))
                              if self.predicate(self.strand, i))
        self.R = self.rate * len(self.indices)

    def perform(self, r):
        # Figure out what part of the strand to update
        # TODO this is probably slow (converting set to list every transition)
        #   could be fixed by using a dict combined with a list instead of a set
        set_index = int(r/self.rate)
        set_value = list(self.indices)[set_index]
#        full_index = set_value + self.offset
        full_index = set_value

        # Update the strand
        self.strand[full_index] = self.new_state

        # Remove this index
        self.indices.remove(set_value)

        # Let everyone else know what changed
        return ('transition', full_index)

    def update(self, transition_output):
        command, value = transition_output
        return self._update_switch[command](value)

    def _update_transition(self, full_index):
        sp = self.predicate
        si = self.indices
        effected_indices = xrange(full_index - sp.pointed_range,
                                   full_index + sp.barbed_range + 1)
        for i in effected_indices:
            if sp(self.strand, i):
                si.add(i)
            else:
                si.discard(i)
        self.R = self.rate * len(self.indices)
    
    def _update_polymerization(self, end):
        # FIXME assumes barbed (ignores argument)
        return self._update_transition(len(self.strand)-1)
#        index = len(self.strand) - 1
#        if self.predicate(self.strand, index):
#            self.indices.add(index)

    def _update_depolymerization(self, end):
        # FIXME assumes barbed (ignores argument)
        self.indices.discard(len(self.strand))
        return self._update_transition(len(self.strand)-1)

class BarbedPolymerization(object):
    def __init__(self, rate, state):
        self.rate  = rate
        self.state = state
        self.R     = rate
    
    def initialize(self, strand):
        self.strand = strand

    def perform(self, r):
        self.strand.append(self.state)
        return ('poly', 'barbed')

    def update(self, transition_output):
        pass

class BarbedDepolymerization(object):
    def __init__(self, rates):
        self.rates  = rates
    
    def initialize(self, strand):
        self.strand = strand
        self.R      = self.rates[strand[-1]]

    def perform(self, r):
        self.strand.pop()
        return ('depoly', 'barbed')

    def update(self, transition_output):
        self.R = self.rates[self.strand[-1]]
