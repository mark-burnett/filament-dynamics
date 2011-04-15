#    Copyright (C) 2011 Mark Burnett
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

from actin_dynamics.numerical import rate_bisect, utils

from .base_classes import Transition
from . import mixins

class ReverseRelease(Transition):
    __slots__ = ['old_state', 'rate', 'concentration', 'new_state',
                 '_last_rs']
    def __init__(self, old_state=None, rate=None, new_state=None,
                 concentration=None, label=None):
        self.old_state = old_state
        self.rate      = rate
        self.new_state = new_state
        self.concentration = concentration

        Transition.__init__(self, label=label)

    def R(self, filaments, concentrations):
        r = self.rate * concentrations[self.concentration].value
        self._last_rs = [r * filament.state_count(self.old_state)
                for filament in filaments]
        return sum(self._last_rs)

    def perform(self, time, filaments, concentrations, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_rs)))
        current_filament = filaments[filament_index]

        target_index = int(remaining_r / self.rate)
        state_index = current_filament.state_index(self.old_state, target_index)

        current_filament[state_index] = self.new_state
        concentrations[self.concentration].remove_monomer(time)
