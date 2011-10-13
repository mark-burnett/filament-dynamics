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

from ...numerical import utils

from .base_classes import FilamentTransition as _FilamentTransition
from . import mixins as _mixins

class CooperativeHydrolysis(_FilamentTransition):
    __slots__ = ['old_state', 'pointed_neighbors', 'rate', 'new_state',
                 'boundary_rates']
    def __init__(self, old_state=None, rate=None, new_state=None, label=None,
                 **cooperativities):
        self.old_state        = old_state
        self.rate             = rate
        self.new_state        = new_state

        for c in cooperativities.itervalues():
            assert c >= 1

        self.pointed_neighbors = cooperativities.keys()
        self.boundary_rates = dict((s, self.rate * (rho - 1))
                                   for s, rho in cooperativities.iteritems())

        _FilamentTransition.__init__(self, label=label)

    def R(self, filaments, concentrations):
        return [sum(self._boundary_rates(filament)) + self._random_rate(filament)
                for filament in filaments]

    def _boundary_rates(self, filament):
        return [filament.boundary_count(self.old_state, pn)
                * self.boundary_rates[pn]
                for pn in self.pointed_neighbors]

    def _random_rate(self, filament):
        return self.rate * filament.state_count(self.old_state)

    def perform(self, time, filaments, concentrations, index, r):
        current_filament = filaments[index]

        random_rate = self._random_rate(current_filament)
        if r < random_rate:
            self._perform_random(time, current_filament, r, random_rate)
        else:
            boundary_rates = self._boundary_rates(current_filament)
            running_rates = list(utils.running_total(boundary_rates))

            boundary_r = r - random_rate
            boundary_index = bisect.bisect_left(running_rates, boundary_r)

            specific_r = running_rates[boundary_index] - boundary_r

            self._perform_boundary(time, current_filament, specific_r,
                                   boundary_rates[boundary_index],
                                   self.pointed_neighbors[boundary_index])

        _FilamentTransition.perform(self, time, filaments, concentrations, index, r)


    def _perform_boundary(self, time, filament, r, boundary_rate, pointed_neighbor):
        target_index = int(r / boundary_rate)
        state_index = filament.boundary_index(self.old_state,
                                              pointed_neighbor,
                                              target_index)
        filament[state_index] = self.new_state

    def _perform_random(self, time, filament, r, random_rate):
        target_index = int(r / random_rate)
        state_index = filament.state_index(self.old_state, target_index)
#        state_index = filament.non_boundary_state_index(self.old_state,
#                                                        self.pointed_neighbors,
#                                                        target_index)
        filament[state_index] = self.new_state


CooperativeHydrolysisWithByproduct = _mixins.add_byproduct(CooperativeHydrolysis)
