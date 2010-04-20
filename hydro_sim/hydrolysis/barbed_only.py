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

__all__ = ['BarbedOnly']

class BarbedOnly(object):
    __slots__ = ['strand', 'indicies', 'R', 'predicate', 'rate', 'new_state', '_update_switch', 'indices']
    def __init__(self, predicate, rate, new_state):
        self.predicate = predicate
        self.rate = rate
        self.new_state = new_state

    def initialize(self, strand):
        self._update_switch = {'hydrolysis': self._update_hydrolysis,
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
        old_state = self.strand[full_index]
        self.strand[full_index] = self.new_state

        # Remove this index
        self.indices.remove(set_value)

        # Let everyone else know what changed
        return ('hydrolysis', ((old_state, self.new_state), full_index))

    def update(self, transition_output):
        command, value = transition_output
        return self._update_switch[command](value)

    def _update_hydrolysis(self, value):
        (old_state, new_state), full_index = value
#        sp = self.predicate
#        si = self.indices
        effected_indices = xrange(full_index - self.predicate.pointed_range,
                                  full_index + self.predicate.barbed_range + 1)
        for i in effected_indices:
            if self.predicate(self.strand, i):
                self.indices.add(i)
            else:
                self.indices.discard(i)
        self.R = self.rate * len(self.indices)
    
    def _update_polymerization(self, value):
        end, state = value
        # NOTE assumes barbed (ignores argument)
        return self._update_hydrolysis(((None, state), len(self.strand)-1))

    def _update_depolymerization(self, value):
        # NOTE assumes barbed (ignores argument)
        self.indices.discard(len(self.strand))
        return self._update_hydrolysis(((None, None), len(self.strand)-1))
