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

class RandomHydrolysis(Transition):
    __slots__ = ['old_species', 'rate', 'new_species', '_last_rs', '_last_names']
    def __init__(self, old_species=None, rate=None, new_species=None, label=None):
        self.old_species = old_species
        self.rate      = rate
        self.new_species = new_species

        Transition.__init__(self, label=label)

    def R(self, filaments, concentrations):
        self._last_names = []
        self._last_rs = []
        for name, filament in filaments.iteritems():
            self._last_names.append(name)
            self._last_rs.append(self.rate * filament.species_count(
                self.old_species))
        return sum(self._last_rs)

    def perform(self, time, filaments, concentrations, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_rs)))
        name = self._last_names[filament_index]
        current_filament = filaments[name]

        target_index = int(remaining_r / self.rate)

        species_index = current_filament.species_index(self.old_species, target_index)

        current_filament[species_index] = self.new_species


RandomHydrolysisWithByproduct = mixins.add_byproduct(RandomHydrolysis)
