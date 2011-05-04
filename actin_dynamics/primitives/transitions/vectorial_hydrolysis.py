#    Copyright (C) 2010-2011 Mark Burnett
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


class VectorialHydrolysis(Transition):
    __slots__ = ['old_species', 'pointed_neighbor', 'rate', 'new_species',
                 '_last_rs', '_last_filaments']
    def __init__(self, old_species=None, pointed_neighbor=None, rate=None,
                 new_species=None, *args, **kwargs):
        self.old_species  = old_species
        self.new_species  = new_species
        self.pointed_neighbor = pointed_neighbor
        self.rate = rate

        Transition.__init__(self, *args, **kwargs)

    def R(self, time, state):
        self._last_filaments = []
        self._last_rs = []
        for filament in state.filaments.itervalues():
            self._last_filaments.append(filament)
            self._last_rs.append(self.rate * filament.boundary_count(
                self.old_species, self.pointed_neighbor))
        return sum(self._last_rs)

    def perform(self, time, state, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_rs)))
        current_filament = self._last_filaments[filament_index]

        target_index = int(remaining_r / self.rate)
        species_index = current_filament.boundary_index(self.old_species,
                                                      self.pointed_neighbor,
                                                      target_index)
        current_filament[species_index] = self.new_species

VectorialHydrolysisWithByproduct = mixins.add_byproduct(VectorialHydrolysis)
