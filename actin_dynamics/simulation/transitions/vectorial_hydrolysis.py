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


class VectorialHydrolysis(_Transition):
    parameters = ['rate']
    states = ['old_state', 'pointed_neighbor', 'new_state']

    __slots__ = ['old_state', 'pointed_neighbor', 'rate', 'new_state']
    def __init__(self, old_state=None, pointed_neighbor=None, rate=None,
                 new_state=None):
        self.old_state        = old_state
        self.pointed_neighbor = pointed_neighbor
        self.rate             = rate
        self.new_state        = new_state

        _Transition.__init__(self)

    def R(self, strand, concentrations):
        return self.rate * len(
                strand.boundary_indices[self.old_state][self.pointed_neighbor])

    def perform(self, time, strand, concentrations, r):
        boundary_index = int(r / self.rate)
        strand_index = (strand.boundary_indices
                [self.old_state][self.pointed_neighbor][boundary_index])
        strand.set_state(strand_index, self.new_state)

        _Transition.perform(self, time, strand, concentrations, r)

VectorialHydrolysisWithByproduct = _mixins.add_byproduct(VectorialHydrolysis)
