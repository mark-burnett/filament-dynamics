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

class RandomHydrolysis(_FilamentTransition):
    __slots__ = ['old_state', 'rate', 'new_state']
    def __init__(self, old_state=None, rate=None, new_state=None, label=None,
            cooperativity=None, melki_a=None, melki_b=None, melki_c=None):
        self.old_state = old_state
        self.rate      = rate
        self.new_state = new_state

        if cooperativity and melki_a and melki_b and melki_c:
            self.rate = _melki_equation.rate(cooperativity,
                    melki_a, melki_b, melki_c)

        _FilamentTransition.__init__(self, label=label)

    def R(self, filaments, concentrations):
        return [self.rate * filament.state_count(self.old_state)
                for filament in filaments]

    def perform(self, time, filaments, concentrations, filament_index, r):
        target_index = int(r / self.rate)
        current_filament = filaments[filament_index]
        state_index = current_filament.state_index(self.old_state, target_index)

#        assert(current_filament.states[state_index] == self.old_state)
        current_filament[state_index] = self.new_state

        _FilamentTransition.perform(self, time, filaments, concentrations,
                                    filament_index, r)


RandomHydrolysisWithByproduct = _mixins.add_byproduct(RandomHydrolysis)
