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

from .base_classes import FilamentTransition as _FilamentTransition
from . import mixins as _mixins


class VectorialHydrolysis(_FilamentTransition):
    __slots__ = ['old_state', 'pointed_neighbor', 'rate', 'new_state']
    def __init__(self, old_state=None, pointed_neighbor=None, rate=None,
                 new_state=None):
        self.old_state        = old_state
        self.pointed_neighbor = pointed_neighbor
        self.rate             = rate
        self.new_state        = new_state

        _FilamentTransition.__init__(self)

    def R(self, filaments, concentrations):
        return [self.rate * filament.boundary_count(self.old_state,
                                                    self.pointed_neighbor)
                for filament in filaments]

    def perform(self, time, filaments, concentrations, index, r):
        current_filament = filaments[index]

        target_index = int(r / self.rate)
        state_index = current_filament.boundary_index(self.old_state,
                                                      self.pointed_neighbor,
                                                      target_index)
        current_filament[state_index] = self.new_state

        _FilamentTransition.perform(self, time, filaments, concentrations, index, r)

VectorialHydrolysisWithByproduct = _mixins.add_byproduct(VectorialHydrolysis)
