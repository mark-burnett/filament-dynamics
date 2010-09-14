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

from .base_classes import Transition as _Transition
from . import mixins as _mixins


class RandomHydrolysis(_Transition):
    # XXX Are we going to use these descriptions?
    description = 'Independent state change.'
    parameters = ['rate', 'number']
    states = ['old_state', 'new_state']

    __slots__ = ['old_state', 'rate', 'new_state']
    def __init__(self, old_state=None, rate=None, new_state=None, number=None):
        self.old_state = old_state
        self.rate      = rate
        self.new_state = new_state

        _Transition.__init__(self, number)

    def R(self, strands, concentrations):
        return [self.rate * len(s.state_indices[self.old_state])
                for s in strands]

    def perform(self, time, strands, concentrations, index, r):
        state_index = int(r / self.rate)
        current_strand = strands[index]
        strand_index = current_strand.state_indices[self.old_state][state_index]
        current_strand.set_state(strand_index, self.new_state)

        _Transition.perform(self, time, strands, concentrations, index, r)


RandomHydrolysisWithByproduct = _mixins.add_byproduct(RandomHydrolysis)
