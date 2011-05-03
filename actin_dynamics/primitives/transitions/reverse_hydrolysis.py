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

class ReverseHydrolysis(Transition):
    __slots__ = ['old_species', 'rate', 'concentration', 'new_species',
                 '_last_er', '_last_rs', '_last_filaments']
    def __init__(self, old_species=None, rate=None, new_species=None,
                 concentration=None, *args, **kwargs):
        self.old_species = old_species
        self.rate        = rate
        self.new_species = new_species
        self.concentration = concentration

        Transition.__init__(self, *args, **kwargs)

    def R(self, time, state):
        self._last_er = (self.rate
                * state.concentrations[self.concentration].value(time))
        self._last_rs = []
        self._last_filaments = []
        for filament in state.filaments.itervalues():
            self._last_rs.append(self._last_er
                    * filament.state_count(self.old_species))
            self._last_filaments.append(filament)
        return sum(self._last_rs)

    def get_current_filament(self, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_rs)))
        return self._last_filaments[filament_index], remaining_r

    def perform(self, time, state, r):
        current_filament, remaining_r = self.get_current_filament(r)
        target_index = int(remaining_r / self._last_er)
        species_index = current_filament.state_index(self.old_species,
                                                     target_index)
        current_filament[species_index] = self.new_species
        state.concentrations[self.concentration].remove_monomer(time)
