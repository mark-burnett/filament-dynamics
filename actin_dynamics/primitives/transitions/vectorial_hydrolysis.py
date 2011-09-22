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

from . import melki_equation as _melki_equation

class VectorialHydrolysis(_FilamentTransition):
    __slots__ = ['old_state', 'pointed_neighbor', 'rate', 'new_state']
    def __init__(self, old_state=None, pointed_neighbor=None, rate=None,
                 new_state=None, label=None, base_rate=None, cooperativity=None,
                melki_a=None, melki_b=None, melki_c=None,
                 subtract_cooperativity=None):
        self.old_state        = old_state
        self.pointed_neighbor = pointed_neighbor
        self.rate             = rate
        self.new_state        = new_state
        if base_rate and cooperativity:
            if subtract_cooperativity:
                cooperativity -= subtract_cooperativity
            self.rate = base_rate * cooperativity

        if cooperativity and melki_a and melki_b and melki_c:
            self.rate = _melki_equation.rate(cooperativity,
                    melki_a, melki_b, melki_c)



        _FilamentTransition.__init__(self, label=label)

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
