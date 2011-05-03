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

import bisect

from actin_dynamics.numerical import rate_bisect, utils

from .base_classes import Transition
from . import mixins

class CooperativeHydrolysis(Transition):
    __slots__ = ['old_species', 'pointed_neighbors', 'rate', 'new_species',
                 'boundary_rates', '_last_brs', '_last_rrs', '_last_RR']
    def __init__(self, old_species=None, rate=None, new_species=None, label=None,
                 **cooperativities):
        self.old_species        = old_species
        self.rate             = rate
        self.new_species        = new_species

        for c in cooperativities.itervalues():
            assert c >= 1

        self.pointed_neighbors = cooperativities.keys()
        self.boundary_rates = dict((s, self.rate * (rho - 1))
                                   for s, rho in cooperativities.iteritems())

        Transition.__init__(self, label=label)

    def R(self, filaments, concentrations):
        self._last_names = filaments.keys()
        return (sum(self._boundary_rates(filaments)) +
                self._random_rate(filaments))

    def _species_boundary_rates(self, filament):
        return [filament.boundary_count(self.old_species, pn) *
                    self.boundary_rates[pn]
                for pn in self.pointed_neighbors]

    def _boundary_rates(self, filaments):
        self._last_brs = []
        for filament in filaments:
            self._last_brs.append(sum(self._species_boundary_rates(filament)))
        return self._last_brs

    def _random_rate(self, filaments):
        self._last_rrs = [self.rate * filament.species_count(self.old_species)
                         for filament in filaments]
        self._last_RR = sum(self._last_rrs)
        return self._last_RR


    def perform(self, time, filaments, concentrations, r):
        if r < self._last_RR:
            self._perform_random(time, filaments, r)
        else:
            remaining_r = r - self._last_RR
            self._perform_boundary(time, filaments, remaining_r)


    def _perform_random(self, time, filaments, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_rrs)))
        current_filament = filaments[filament_index]
        target_index = int(remaining_r / self.rate)

        species_index = current_filament.species_index(self.old_species, target_index)

        current_filament[species_index] = self.new_species


    def _perform_boundary(self, time, filaments, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_brs)))
        current_filament = filaments[filament_index]

        self._perform_boundary_species(time, current_filament, remaining_r)

    def _perform_boundary_species(self, time, filament, r):
        species_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._species_boundary_rates(filament))))

        pointed_neighbor = self.pointed_neighbors[species_index]
        target_index = int(remaining_r / self.boundary_rates[pointed_neighbor])
        species_index = filament.boundary_index(self.old_species,
                                              pointed_neighbor,
                                              target_index)
        filament[species_index] = self.new_species


CooperativeHydrolysisWithByproduct = mixins.add_byproduct(CooperativeHydrolysis)
