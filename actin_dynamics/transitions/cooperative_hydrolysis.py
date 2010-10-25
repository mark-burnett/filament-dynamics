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

class CooperativeHydrolysis(_FilamentTransition):
    __slots__ = ['old_state', 'pointed_neighbor', 'rate', 'cooperativity',
                 'new_state']
    def __init__(self, old_state=None, pointed_neighbor=None, rate=None,
            cooperativity=None, new_state=None):
        self.old_state        = old_state
        self.pointed_neighbor = pointed_neighbor
        self.rate             = rate
        self.cooperativity    = cooperativity
        self.new_state        = new_state

        _FilamentTransition.__init__(self)

    def R(self, filaments, concentrations):
        return [self._boundary_rate(filament) + self._random_rate(filament)
                for filament in filaments]

    def _boundary_rate(self, filament):
        boundary_count = len(filament.boundary_indices
                [self.old_state][self.pointed_neighbor])
        return self.rate * self.cooperativity * boundary_count

    def _random_rate(self, filament):
        # XXX Slight repeatition of code, but convenient.
        boundary_count = len(filament.boundary_indices
                [self.old_state][self.pointed_neighbor])
        protomer_count = len(filament.state_indices[self.old_state])
        random_count = protomer_count - boundary_count

        return self.rate * random_count


    def perform(self, time, filaments, concentrations, index, r):
        current_filament = filaments[index]

        boundary_rate = self._boundary_rate(current_filament)
        random_rate = self._random_rate(current_filament)

        if r < boundary_rate:
            self._perform_boundary(time, current_filament, concentrations, r,
                                   boundary_rate)
        else:
            self._perform_random(time, current_filament, concentrations,
                                 r - boundary_rate, random_rate)

        _FilamentTransition.perform(self, time, filaments, concentrations, index, r)

    def _perform_boundary(self, time, filament, concentrations, r, boundary_rate):
        boundary_index = int(r / boundary_rate)
        filament_index = (filament.boundary_indices
                [self.old_state][self.pointed_neighbor][boundary_index])
        filament.set_state(filament_index, self.new_state)

    def _perform_random(self, time, filament, concentrations, r, random_rate):
        target_index = int(r / self.rate)
        current_index = -1

        for working_index in filament.state_indices[self.old_state]:
            # XXX Performance warning:  boundary_indices should probably contain sets
            if working_index not in (filament.boundary_indices[self.old_state]
                                     [self.pointed_neighbor]):
                current_index += 1
                if target_index == current_index:
                    filament.set_state(working_index, self.new_state)
                    return
        raise IndexError('No working index found.')


CooperativeHydrolysisWithByproduct = _mixins.add_byproduct(CooperativeHydrolysis)
